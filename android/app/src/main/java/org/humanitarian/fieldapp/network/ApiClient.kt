package org.humanitarian.fieldapp.network

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.humanitarian.fieldapp.models.FieldReport
import org.humanitarian.fieldapp.models.OrgRequest
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL

sealed class ApiResult<out T> {
    data class Success<T>(val data: T) : ApiResult<T>()
    data class Error(val message: String) : ApiResult<Nothing>()
}

object ApiClient {

    // Candidate URLs for USB ADB Reverse Tunnel (127.0.0.1:8000) & Wi-Fi LAN
    private val CANDIDATE_BASE_URLS = listOf(
        "http://127.0.0.1:8000",    // USB ADB Reverse tunnel (Primary)
        "http://172.16.58.76:8000", // Wi-Fi LAN Host IP
        "http://10.0.2.2:8000",     // Emulator host alias
        "http://10.142.1.84:8000"   // Secondary Wi-Fi LAN IP
    )

    private var activeBaseUrl = CANDIDATE_BASE_URLS.first()

    // Helper: Attempts request across candidate hosts until connection succeeds
    private fun <T> executeWithFailover(block: (baseUrl: String) -> ApiResult<T>): ApiResult<T> {
        val candidates = listOf(activeBaseUrl) + CANDIDATE_BASE_URLS.filter { it != activeBaseUrl }
        var lastError: ApiResult.Error = ApiResult.Error("Network unreachable")

        for (host in candidates) {
            val result = block(host)
            if (result is ApiResult.Success) {
                activeBaseUrl = host
                return result
            } else if (result is ApiResult.Error) {
                lastError = result
            }
        }
        return lastError
    }

    // ───────────── INTERNET CHANNEL ─────────────

    suspend fun postNeed(report: FieldReport): ApiResult<String> {
        return withContext(Dispatchers.IO) {
            executeWithFailover { host ->
                var connection: HttpURLConnection? = null
                try {
                    val url = URL("$host/api/v1/needs")
                    connection = url.openConnection() as HttpURLConnection
                    connection.requestMethod = "POST"
                    connection.connectTimeout = 3000
                    connection.readTimeout = 3000
                    connection.setRequestProperty("Content-Type", "application/json")
                    connection.doOutput = true

                    val payload = JSONObject()
                        .put("type", "need")
                        .put("organization_id", report.organizationId)
                        .put("location_code", report.locationCode)
                        .put("location_name", locationName(report.locationCode))
                        .put("location", locationName(report.locationCode))
                        .put("resource", resourceName(report.resourceCode))
                        .put("resource_code", report.resourceCode)
                        .put("quantity", report.quantity)
                        .put("urgency", urgencyName(report.urgencyCode))
                        .put("urgency_code", report.urgencyCode)
                        .put("notes", report.notes)
                        .put("source", "android")
                        .put("latitude", report.latitude ?: 0.0)
                        .put("longitude", report.longitude ?: 0.0)

                    connection.outputStream.use { outputStream ->
                        outputStream.write(payload.toString().toByteArray())
                        outputStream.flush()
                    }

                    val responseCode = connection.responseCode
                    val responseBody = if (responseCode in 200..299) {
                        connection.inputStream.bufferedReader().use { it.readText() }
                    } else {
                        connection.errorStream?.bufferedReader()?.use { it.readText() } ?: ""
                    }

                    if (responseCode in 200..299) ApiResult.Success(responseBody.ifBlank { "HTTP $responseCode" })
                    else ApiResult.Error("HTTP $responseCode: ${responseBody.take(200)}")
                } catch (exception: Exception) {
                    ApiResult.Error(exception.message ?: "Network request failed")
                } finally {
                    connection?.disconnect()
                }
            }
        }
    }

    // ───────────── SMS GATEWAY CHANNEL ─────────────

    suspend fun postSmsWebhook(smsPayload: String): ApiResult<String> {
        return withContext(Dispatchers.IO) {
            executeWithFailover { host ->
                var connection: HttpURLConnection? = null
                try {
                    val url = URL("$host/api/v1/sms/webhook")
                    connection = url.openConnection() as HttpURLConnection
                    connection.requestMethod = "POST"
                    connection.connectTimeout = 3000
                    connection.readTimeout = 3000
                    connection.setRequestProperty("Content-Type", "application/json")
                    connection.doOutput = true

                    val payload = JSONObject().put("sms", smsPayload)

                    connection.outputStream.use { outputStream ->
                        outputStream.write(payload.toString().toByteArray())
                        outputStream.flush()
                    }

                    val responseCode = connection.responseCode
                    val responseBody = if (responseCode in 200..299) {
                        connection.inputStream.bufferedReader().use { it.readText() }
                    } else {
                        connection.errorStream?.bufferedReader()?.use { it.readText() } ?: ""
                    }

                    if (responseCode in 200..299) ApiResult.Success(responseBody)
                    else ApiResult.Error("HTTP $responseCode: ${responseBody.take(200)}")
                } catch (exception: Exception) {
                    ApiResult.Error(exception.message ?: "SMS gateway unreachable")
                } finally {
                    connection?.disconnect()
                }
            }
        }
    }

    suspend fun getSmsInbox(): ApiResult<List<String>> {
        return withContext(Dispatchers.IO) {
            executeWithFailover { host ->
                var connection: HttpURLConnection? = null
                try {
                    val url = URL("$host/api/v1/sms/inbox")
                    connection = url.openConnection() as HttpURLConnection
                    connection.requestMethod = "GET"
                    connection.connectTimeout = 3000
                    connection.readTimeout = 3000

                    val responseCode = connection.responseCode
                    if (responseCode in 200..299) {
                        val body = connection.inputStream.bufferedReader().use { it.readText() }
                        val json = JSONObject(body)
                        val messagesArray = json.getJSONArray("messages")
                        val messages = mutableListOf<String>()
                        for (i in 0 until messagesArray.length()) {
                            messages.add(messagesArray.getString(i))
                        }
                        ApiResult.Success(messages)
                    } else {
                        ApiResult.Error("HTTP $responseCode")
                    }
                } catch (e: Exception) {
                    ApiResult.Error(e.message ?: "Inbox fetch failed")
                } finally {
                    connection?.disconnect()
                }
            }
        }
    }

    suspend fun clearInbox(): ApiResult<String> {
        return withContext(Dispatchers.IO) {
            executeWithFailover { host ->
                var connection: HttpURLConnection? = null
                try {
                    val url = URL("$host/api/v1/sms/clear")
                    connection = url.openConnection() as HttpURLConnection
                    connection.requestMethod = "POST"
                    connection.connectTimeout = 3000
                    connection.readTimeout = 3000
                    connection.responseCode
                    ApiResult.Success("cleared")
                } catch (e: Exception) {
                    ApiResult.Error(e.message ?: "Clear failed")
                } finally {
                    connection?.disconnect()
                }
            }
        }
    }

    // ───────────── REAL-TIME LOCATION + STATUS POLLING ─────────────

    suspend fun postLocationUpdate(organizationId: String, lat: Double, lng: Double): ApiResult<String> {
        return withContext(Dispatchers.IO) {
            executeWithFailover { host ->
                var connection: HttpURLConnection? = null
                try {
                    val url = URL("$host/api/v1/location/update")
                    connection = url.openConnection() as HttpURLConnection
                    connection.requestMethod = "POST"
                    connection.connectTimeout = 3000
                    connection.readTimeout = 3000
                    connection.setRequestProperty("Content-Type", "application/json")
                    connection.doOutput = true

                    val payload = JSONObject()
                        .put("organization_id", organizationId)
                        .put("latitude", lat)
                        .put("longitude", lng)

                    connection.outputStream.use { it.write(payload.toString().toByteArray()); it.flush() }

                    val code = connection.responseCode
                    if (code in 200..299) ApiResult.Success("ok")
                    else ApiResult.Error("HTTP $code")
                } catch (e: Exception) {
                    ApiResult.Error(e.message ?: "Location update failed")
                } finally {
                    connection?.disconnect()
                }
            }
        }
    }

    suspend fun getRequestsByOrg(organizationId: String): ApiResult<List<OrgRequest>> {
        return withContext(Dispatchers.IO) {
            executeWithFailover { host ->
                var connection: HttpURLConnection? = null
                try {
                    val url = URL("$host/api/v1/requests/by-org/$organizationId")
                    connection = url.openConnection() as HttpURLConnection
                    connection.requestMethod = "GET"
                    connection.connectTimeout = 3000
                    connection.readTimeout = 3000

                    val code = connection.responseCode
                    if (code in 200..299) {
                        val body = connection.inputStream.bufferedReader().use { it.readText() }
                        val arr = JSONObject(body).getJSONArray("requests")
                        val list = mutableListOf<OrgRequest>()
                        for (i in 0 until arr.length()) {
                            val o = arr.getJSONObject(i)
                            list.add(
                                OrgRequest(
                                    id = o.optString("id", ""),
                                    type = o.optString("type", ""),
                                    resource = o.optString("resource", ""),
                                    quantity = o.optInt("quantity", 0),
                                    status = o.optString("status", "pending"),
                                    allocatedProvider = if (o.isNull("allocated_provider")) null else o.optString("allocated_provider", ""),
                                    allocatedCargo = if (o.isNull("allocated_cargo")) null else o.optString("allocated_cargo", ""),
                                    etaHours = if (o.isNull("eta_hours")) null else o.optDouble("eta_hours"),
                                    planId = if (o.isNull("plan_id")) null else o.optString("plan_id", ""),
                                    latitude = if (o.isNull("latitude")) null else o.optDouble("latitude"),
                                    longitude = if (o.isNull("longitude")) null else o.optDouble("longitude"),
                                    createdAt = o.optString("created_at", "")
                                )
                            )
                        }
                        ApiResult.Success(list)
                    } else {
                        ApiResult.Error("HTTP $code")
                    }
                } catch (e: Exception) {
                    ApiResult.Error(e.message ?: "Status fetch failed")
                } finally {
                    connection?.disconnect()
                }
            }
        }
    }

    suspend fun getAssignedMissionsForDonor(providerId: String): ApiResult<List<OrgRequest>> {
        return withContext(Dispatchers.IO) {
            executeWithFailover { host ->
                var connection: HttpURLConnection? = null
                try {
                    val url = URL("$host/api/v1/matches?provider_id=$providerId&limit=25")
                    connection = url.openConnection() as HttpURLConnection
                    connection.requestMethod = "GET"
                    connection.connectTimeout = 3000
                    connection.readTimeout = 3000

                    val code = connection.responseCode
                    if (code in 200..299) {
                        val body = connection.inputStream.bufferedReader().use { it.readText() }
                        val arr = JSONObject(body).getJSONArray("matches")
                        val list = mutableListOf<OrgRequest>()
                        for (i in 0 until arr.length()) {
                            val m = arr.getJSONObject(i)
                            val planId = m.optString("match_id", "")
                            val uid = m.optString("uid", "Citizen")
                            val sit = m.optString("situation", "Emergency Response")
                            val deliveryStatus = m.optString("delivery_status", m.optString("status", "allocated"))

                            val itemsObj = m.optJSONObject("items")
                            var cargoStr = ""
                            var totalQty = 1
                            if (itemsObj != null) {
                                val keys = itemsObj.keys()
                                val itemsList = mutableListOf<String>()
                                while (keys.hasNext()) {
                                    val k = keys.next()
                                    val q = itemsObj.optInt(k, 1)
                                    totalQty = q
                                    itemsList.add("$q ${k.replace('_', ' ')}")
                                }
                                cargoStr = itemsList.joinToString(", ")
                            }

                            val geoObj = m.optJSONObject("request_geo")
                            var lat: Double? = null
                            var lon: Double? = null
                            if (geoObj != null) {
                                val coords = geoObj.optJSONArray("coordinates")
                                if (coords != null && coords.length() >= 2) {
                                    lon = coords.optDouble(0)
                                    lat = coords.optDouble(1)
                                }
                            }

                            list.add(
                                OrgRequest(
                                    id = planId,
                                    type = sit,
                                    resource = if (cargoStr.isNotBlank()) cargoStr else "Relief Supplies",
                                    quantity = totalQty,
                                    status = deliveryStatus,
                                    allocatedProvider = m.optString("provider_name", providerId),
                                    allocatedCargo = cargoStr,
                                    etaHours = m.optDouble("eta_hours", 1.0),
                                    planId = planId,
                                    latitude = lat,
                                    longitude = lon,
                                    createdAt = m.optString("created_at", "")
                                )
                            )
                        }
                        ApiResult.Success(list)
                    } else {
                        ApiResult.Error("HTTP $code")
                    }
                } catch (e: Exception) {
                    ApiResult.Error(e.message ?: "Missions fetch failed")
                } finally {
                    connection?.disconnect()
                }
            }
        }
    }

    suspend fun updateMissionStatus(planId: String, statusCode: String, statusName: String): ApiResult<String> {
        return withContext(Dispatchers.IO) {
            executeWithFailover { host ->
                var connection: HttpURLConnection? = null
                try {
                    val url = URL("$host/api/v1/pact/ingest")
                    connection = url.openConnection() as HttpURLConnection
                    connection.requestMethod = "POST"
                    connection.connectTimeout = 3000
                    connection.readTimeout = 3000
                    connection.setRequestProperty("Content-Type", "application/json")
                    connection.doOutput = true

                    val frame = "S|001|$planId|$statusCode|00"
                    val payload = JSONObject().put("payload", frame)

                    connection.outputStream.use { it.write(payload.toString().toByteArray()); it.flush() }

                    val code = connection.responseCode
                    if (code in 200..299) ApiResult.Success("Status updated to $statusName")
                    else ApiResult.Error("HTTP $code")
                } catch (e: Exception) {
                    ApiResult.Error(e.message ?: "Status update failed")
                } finally {
                    connection?.disconnect()
                }
            }
        }
    }

    // ───────────── MAPPINGS ─────────────

    private fun resourceName(code: String): String {
        return when (code) {
            "F" -> "food_kits"; "W" -> "water_kits"; "M" -> "medical_kits"
            "T" -> "tents"; "B" -> "blankets"; "H" -> "hygiene_kits"
            "D" -> "medical_teams"; else -> "unknown"
        }
    }

    private fun urgencyName(code: String): String {
        return when (code) {
            "L" -> "low"; "M" -> "medium"; "H" -> "high"; "C" -> "critical"; else -> "unknown"
        }
    }

    private fun locationName(code: String): String {
        return when (code) {
            "RA" -> "Region A"; "RB" -> "Region B"; "RC" -> "Region C"
            "D1" -> "District North"; "D2" -> "District South"; else -> code
        }
    }
}