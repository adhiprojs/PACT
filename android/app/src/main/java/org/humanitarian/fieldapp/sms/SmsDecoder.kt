package org.humanitarian.fieldapp.sms

import org.json.JSONObject
import java.util.LinkedHashMap

object SmsDecoder {

    data class DecodedSms(
        val valid: Boolean,
        val typeLabel: String,
        val typeCode: String,
        val message: String,                       // Human-readable sentence
        val fields: LinkedHashMap<String, String>,
        val json: String,
        val checksumValid: Boolean,
        val error: String
    )

    // Taxonomy mappings
    private val situationNames = mapOf(
        '0' to "General Emergency",
        '1' to "Flood / Rising Water",
        '2' to "Earthquake / Debris",
        '3' to "Fire / Explosion",
        '4' to "Landslide / Mudslide",
        '5' to "Building Collapse",
        '6' to "Cyclone / Hurricane",
        '7' to "Hazardous / Chemical",
        '8' to "Heatwave / Drought"
    )

    private val headcountNames = mapOf(
        '0' to "1 person",
        '1' to "2-3 people",
        '2' to "4-5 people",
        '3' to "6-10 people",
        '4' to "11-20 people",
        '5' to "21-50 people",
        '6' to "50+ people"
    )

    private val injuryNames = mapOf(
        '0' to "No injuries",
        '1' to "Minor injuries",
        '2' to "Moderate trauma / fractures",
        '3' to "Severe trauma / bleeding",
        '4' to "Critical / Fatalities"
    )

    private val mobilityNames = mapOf(
        '0' to "Fully mobile",
        '1' to "Limited mobility",
        '2' to "Trapped in debris",
        '3' to "Waterbound / rooftop",
        '4' to "Bedridden"
    )

    private val locationNames = mapOf(
        "RA" to "Region A", "RB" to "Region B", "RC" to "Region C",
        "D1" to "District North", "D2" to "District South"
    )
    private val resourceNames = mapOf(
        "F" to "food_kits", "W" to "water_kits", "M" to "medical_kits",
        "T" to "tents", "B" to "blankets", "H" to "hygiene_kits",
        "X" to "rescue_teams", "V" to "evac_transport", "P" to "power_generators",
        "I" to "infant_kits", "D" to "medical_teams", "E" to "heavy_equipment", "U" to "unknown"
    )
    private val urgencyNames = mapOf("L" to "low", "M" to "medium", "H" to "high", "C" to "critical")
    private val statusNames = mapOf(
        "0" to "assigned", "1" to "dispatched", "2" to "in_transit",
        "3" to "delivered", "4" to "blocked", "5" to "cancelled"
    )
    private val availabilityNames = mapOf("A" to "available", "L" to "limited", "U" to "unavailable")

    fun decode(raw: String): DecodedSms {
        val message = raw.trim()
        if (message.isEmpty()) return errorResult("Empty message")
        val parts = message.split("|")
        if (parts.size < 2) return errorResult("Invalid format: too few fields")
        return when (parts[0].trim().uppercase()) {
            "Q" -> decodeQ(parts, message)
            "C" -> decodeConfirmation(parts, message)
            "N" -> decodeNeed(parts, message)
            "R" -> decodeResource(parts, message)
            "A" -> decodeAllocation(parts, message)
            "S" -> decodeStatus(parts, message)
            "M" -> decodeMarker(parts, message)
            "X" -> decodeCancel(parts, message)
            else -> errorResult("Unknown message type: ${parts[0]}")
        }
    }

    private fun checksumOk(fullMessage: String, providedCrc: String): Boolean {
        val body = fullMessage.substringBeforeLast("|")
        return xorChecksum(body).equals(providedCrc.trim(), ignoreCase = true)
    }

    private fun pretty(json: JSONObject): String = json.toString(2)

    private fun errorResult(msg: String): DecodedSms {
        return DecodedSms(false, "Error", "", "", LinkedHashMap(), "", false, msg)
    }

    /**
     * Decodes Q Citizen / Emergency SOS Frame:
     * Q|SEQ|UID|PAYLOAD_10|PACK10_GPS|CRC
     */
    private fun decodeQ(parts: List<String>, full: String): DecodedSms {
        if (parts.size < 6) return errorResult("Invalid Q frame (expected Q|SEQ|UID|PAYLOAD|GEO|CRC)")

        val seq = parts[1].trim()
        val uid = parts[2].trim()
        val payloadStr = parts[3].trim().uppercase()
        val geoStr = parts[4].trim().uppercase()
        val crc = parts[5].trim()
        val crcOk = checksumOk(full, crc)

        var lat = 0.0
        var lon = 0.0
        var geoFormatted = geoStr
        try {
            if (geoStr.length >= 10) {
                val geo = Pack10.decode(geoStr)
                lat = geo.latitude
                lon = geo.longitude
                geoFormatted = "Lat: ${"%.5f".format(lat)}, Lon: ${"%.5f".format(lon)}"
            }
        } catch (_: Exception) {}

        var sitName = "Emergency"
        var hcName = "1 person"
        var injName = "Uninjured"
        var mobName = "Mobile"
        var urgName = "Medium"
        val requestedResources = mutableListOf<String>()

        if (payloadStr.length >= 10) {
            sitName = situationNames[payloadStr[1]] ?: "General Emergency"
            hcName = headcountNames[payloadStr[2]] ?: "1 person"
            injName = injuryNames[payloadStr[3]] ?: "No injuries"
            mobName = mobilityNames[payloadStr[4]] ?: "Fully mobile"
            urgName = urgencyNames[payloadStr[5].toString()]?.replaceFirstChar { it.uppercase() } ?: "Medium"

            try {
                val needsInt = Base36.decode(payloadStr.substring(6, 9))
                if ((needsInt and (1L shl 0)) > 0) requestedResources.add("Food")
                if ((needsInt and (1L shl 1)) > 0) requestedResources.add("Water")
                if ((needsInt and (1L shl 2)) > 0) requestedResources.add("Medical Kits")
                if ((needsInt and (1L shl 3)) > 0) requestedResources.add("Tents")
                if ((needsInt and (1L shl 4)) > 0) requestedResources.add("Blankets")
                if ((needsInt and (1L shl 5)) > 0) requestedResources.add("Hygiene Kits")
                if ((needsInt and (1L shl 6)) > 0) requestedResources.add("Rescue Team")
                if ((needsInt and (1L shl 7)) > 0) requestedResources.add("Evac Transport")
                if ((needsInt and (1L shl 8)) > 0) requestedResources.add("Generators")
                if ((needsInt and (1L shl 9)) > 0) requestedResources.add("Infant Kits")
                if ((needsInt and (1L shl 10)) > 0) requestedResources.add("Doctors")
                if ((needsInt and (1L shl 11)) > 0) requestedResources.add("Heavy Equipment")
            } catch (_: Exception) {}
        }

        val resSummary = if (requestedResources.isNotEmpty()) requestedResources.joinToString(", ") else "General Aid"
        val humanSentence = "🚨 [SOS Target $uid]: $sitName involving $hcName. Status: $injName, $mobName. Urgency: $urgName. Needs: $resSummary. Location: ($lat, $lon)."

        val fields = LinkedHashMap<String, String>().apply {
            put("Type", "Emergency SOS (Q)")
            put("Sequence", seq)
            put("Target UID", uid)
            put("Coordinates", geoFormatted)
            put("Situation", sitName)
            put("Population", hcName)
            put("Casualties", injName)
            put("Mobility", mobName)
            put("Urgency", urgName)
            put("Needed Supplies", resSummary)
            put("Checksum", if (crcOk) "$crc (VALID)" else "$crc (INVALID)")
        }

        val json = JSONObject().apply {
            put("type", "individual_request")
            put("seq", seq)
            put("uid", uid)
            put("situation", sitName)
            put("headcount", hcName)
            put("injury", injName)
            put("mobility", mobName)
            put("urgency", urgName)
            put("needed_resources", requestedResources)
            put("latitude", lat)
            put("longitude", lon)
            put("pack10", geoStr)
            put("checksum_valid", crcOk)
        }

        return DecodedSms(true, "Emergency SOS", "Q", humanSentence, fields, pretty(json), crcOk, "")
    }

    /**
     * Decodes C Confirmation ACK frame:
     * C|SEQ|UID|PLAN_ID|STATE|ETA|CRC or C|SEQ|REF|RESULT|CRC
     */
    private fun decodeConfirmation(parts: List<String>, full: String): DecodedSms {
        val seq = parts.getOrNull(1) ?: "001"
        val uid = if (parts.size >= 7) parts[2] else "CIT00"
        val planId = if (parts.size >= 7) parts[3] else (parts.getOrNull(2) ?: "PLAN")
        val state = if (parts.size >= 7) parts[4] else (parts.getOrNull(3) ?: "OK")
        val eta = if (parts.size >= 7) parts[5] else "0"
        val crc = parts.lastOrNull() ?: ""
        val crcOk = checksumOk(full, crc)

        val humanSentence = "✅ Dispatch Plan '$planId' committed for $uid. Status: ${state.uppercase()}, Estimated arrival: $eta hours."

        val fields = LinkedHashMap<String, String>().apply {
            put("Type", "Confirmation ACK (C)")
            put("Sequence", seq)
            put("Recipient UID", uid)
            put("Plan ID", planId)
            put("Commit Status", state.uppercase())
            put("ETA (Hours)", eta)
            put("Checksum", if (crcOk) "$crc (VALID)" else "$crc (INVALID)")
        }

        val json = JSONObject().apply {
            put("type", "confirmation")
            put("seq", seq)
            put("uid", uid)
            put("plan_id", planId)
            put("status", state)
            put("eta_hours", eta.toDoubleOrNull() ?: 0.0)
            put("checksum_valid", crcOk)
        }

        return DecodedSms(true, "Confirmation ACK", "C", humanSentence, fields, pretty(json), crcOk, "")
    }

    private fun decodeNeed(parts: List<String>, full: String): DecodedSms {
        if (parts.size < 8) return errorResult("Invalid Need format (expected N|SEQ|ORG|LOC|RES|QTY|URG|CRC)")
        val seq = parts[1].trim()
        val org = parts[2].trim()
        val loc = parts[3].trim()
        val res = parts[4].trim()
        val qty = parts[5].trim().toIntOrNull() ?: 0
        val urg = parts[6].trim()
        val crc = parts[7].trim()
        val crcOk = checksumOk(full, crc)

        var locDisplay = locationNames[loc] ?: loc
        if (loc.length == 10 && !locationNames.containsKey(loc)) {
            try {
                val geo = Pack10.decode(loc)
                locDisplay = "Coords (${geo.latitude}, ${geo.longitude})"
            } catch (_: Exception) {}
        }

        val resDisplay = resourceNames[res] ?: res
        val urgDisplay = urgencyNames[urg]?.replaceFirstChar { it.uppercase() } ?: urg

        val humanSentence = "Organization $org reports an urgent need of $qty $resDisplay at $locDisplay (Urgency: $urgDisplay)."

        val fields = LinkedHashMap<String, String>().apply {
            put("Type", "Need Request (N)")
            put("Sequence", seq)
            put("Organization", org)
            put("Location", locDisplay)
            put("Resource", resDisplay)
            put("Quantity", qty.toString())
            put("Urgency", urgDisplay)
            put("Checksum", if (crcOk) "$crc (VALID)" else "$crc (INVALID)")
        }

        val json = JSONObject().apply {
            put("type", "need")
            put("seq", seq)
            put("organization", org)
            put("location", loc)
            put("resource", resDisplay)
            put("quantity", qty)
            put("urgency", urgDisplay.lowercase())
            put("checksum_valid", crcOk)
        }

        return DecodedSms(true, "Need Request", "N", humanSentence, fields, pretty(json), crcOk, "")
    }

    private fun decodeResource(parts: List<String>, full: String): DecodedSms {
        if (parts.size < 8) return errorResult("Invalid Resource format")
        val seq = parts[1].trim()
        val org = parts[2].trim()
        val loc = parts[3].trim()
        val res = parts[4].trim()
        val qty = parts[5].trim().toIntOrNull() ?: 0
        val avail = parts[6].trim()
        val crc = parts[7].trim()
        val crcOk = checksumOk(full, crc)

        val humanSentence = "Provider $org offers $qty ${resourceNames[res] ?: res} at ${locationNames[loc] ?: loc} (Status: ${availabilityNames[avail] ?: avail})."

        val fields = LinkedHashMap<String, String>().apply {
            put("Type", "Resource Availability (R)")
            put("Sequence", seq)
            put("Provider", org)
            put("Location", locationNames[loc] ?: loc)
            put("Resource", resourceNames[res] ?: res)
            put("Quantity", qty.toString())
            put("Status", availabilityNames[avail] ?: avail)
            put("Checksum", if (crcOk) "$crc (VALID)" else "$crc (INVALID)")
        }

        val json = JSONObject().apply {
            put("type", "resource")
            put("seq", seq)
            put("provider", org)
            put("quantity", qty)
            put("checksum_valid", crcOk)
        }

        return DecodedSms(true, "Resource Availability", "R", humanSentence, fields, pretty(json), crcOk, "")
    }

    private fun decodeAllocation(parts: List<String>, full: String): DecodedSms {
        if (parts.size < 9) return errorResult("Invalid Allocation format")
        val seq = parts[1].trim()
        val plan = parts[2].trim()
        val org = parts[3].trim()
        val res = parts[4].trim()
        val qty = parts[5].trim()
        val dest = parts[6].trim()
        val eta = parts[7].trim()
        val crc = parts[8].trim()
        val crcOk = checksumOk(full, crc)

        val humanSentence = "Plan $plan: $org allocated $qty ${resourceNames[res] ?: res} to ${locationNames[dest] ?: dest} (ETA: ${eta}h)."

        val fields = LinkedHashMap<String, String>().apply {
            put("Type", "Allocation Assignment (A)")
            put("Sequence", seq)
            put("Plan ID", plan)
            put("Assigned Org", org)
            put("Supplies", "$qty ${resourceNames[res] ?: res}")
            put("Destination", locationNames[dest] ?: dest)
            put("ETA", "${eta}h")
            put("Checksum", if (crcOk) "$crc (VALID)" else "$crc (INVALID)")
        }

        val json = JSONObject().apply {
            put("type", "allocation")
            put("plan_id", plan)
            put("organization", org)
            put("quantity", qty.toIntOrNull() ?: 0)
            put("eta_hours", eta.toDoubleOrNull() ?: 1.0)
            put("checksum_valid", crcOk)
        }

        return DecodedSms(true, "Allocation", "A", humanSentence, fields, pretty(json), crcOk, "")
    }

    private fun decodeStatus(parts: List<String>, full: String): DecodedSms {
        val seq = parts[1].trim()
        val plan = parts[2].trim()
        val statusCode = parts[3].trim()
        val crc = parts.getOrNull(4)?.trim() ?: ""
        val crcOk = if (crc.isNotBlank()) checksumOk(full, crc) else true
        val statusText = statusNames[statusCode] ?: "unknown"

        val humanSentence = "Delivery status for plan $plan updated to ${statusText.uppercase()}."

        val fields = LinkedHashMap<String, String>().apply {
            put("Type", "Status Update (S)")
            put("Sequence", seq)
            put("Plan ID", plan)
            put("Status", statusText.replaceFirstChar { it.uppercase() })
            put("Checksum", if (crcOk) "$crc (VALID)" else "$crc (INVALID)")
        }

        val json = JSONObject().apply {
            put("type", "status")
            put("plan_id", plan)
            put("status", statusText)
            put("checksum_valid", crcOk)
        }

        return DecodedSms(true, "Status Update", "S", humanSentence, fields, pretty(json), crcOk, "")
    }

    private fun decodeMarker(parts: List<String>, full: String): DecodedSms {
        val seq = parts.getOrNull(1) ?: "001"
        val markerId = parts.getOrNull(2) ?: "M01"
        val mType = parts.getOrNull(3) ?: "CR"
        val loc = parts.getOrNull(4) ?: "RA"
        val crc = parts.lastOrNull() ?: ""
        val crcOk = checksumOk(full, crc)

        val humanSentence = "Map marker $markerId registered at $loc."

        val fields = LinkedHashMap<String, String>().apply {
            put("Type", "Map Marker (M)")
            put("Marker ID", markerId)
            put("Marker Type", mType)
            put("Location", loc)
            put("Checksum", if (crcOk) "$crc (VALID)" else "$crc (INVALID)")
        }

        val json = JSONObject().apply {
            put("type", "marker")
            put("marker_id", markerId)
            put("checksum_valid", crcOk)
        }

        return DecodedSms(true, "Map Marker", "M", humanSentence, fields, pretty(json), crcOk, "")
    }

    private fun decodeCancel(parts: List<String>, full: String): DecodedSms {
        val seq = parts.getOrNull(1) ?: "001"
        val ref = parts.getOrNull(2) ?: "REF"
        val reason = parts.getOrNull(3) ?: "Cancelled by dispatcher"
        val crc = parts.lastOrNull() ?: ""
        val crcOk = checksumOk(full, crc)

        val humanSentence = "Request/Plan $ref was CANCELLED. Reason: $reason."

        val fields = LinkedHashMap<String, String>().apply {
            put("Type", "Cancel Request (X)")
            put("Reference", ref)
            put("Reason", reason)
            put("Checksum", if (crcOk) "$crc (VALID)" else "$crc (INVALID)")
        }

        val json = JSONObject().apply {
            put("type", "cancel")
            put("reference", ref)
            put("reason", reason)
            put("checksum_valid", crcOk)
        }

        return DecodedSms(true, "Cancel Request", "X", humanSentence, fields, pretty(json), crcOk, "")
    }
}