package org.humanitarian.fieldapp.sms

import android.content.Context
import org.humanitarian.fieldapp.models.FieldReport

object SmsEncoder {

    private const val PREFS_NAME = "pact_sms"

    fun nextSequence(
        context: Context,
        organizationId: String
    ): String {
        val safeOrganizationId = organizationId
            .trim()
            .uppercase()
            .ifBlank { "UNKNOWN" }

        val prefs = context.getSharedPreferences(
            PREFS_NAME,
            Context.MODE_PRIVATE
        )

        val key = "sms_seq_$safeOrganizationId"
        val current = prefs.getInt(key, 1)

        val formatted = current.toString().padStart(3, '0')

        val next = if (current >= 999) {
            1
        } else {
            current + 1
        }

        prefs.edit()
            .putInt(key, next)
            .apply()

        return formatted
    }

    /**
     * Encodes a 10-character Base-36 Requester Payload.
     * Schema: [Version(1)][Situation(1)][Headcount(1)][Injury(1)][Mobility(1)][Urgency(1)][Needs(3)][Vuln(1)]
     */
    fun encodeRequesterPayload(
        situationCode: String = "0",
        headcountCode: String = "0",
        injuryCode: String = "0",
        mobilityCode: String = "0",
        urgencyCode: String = "M",
        needsBitfield: Long = 1L, // default bit 0 = Food
        vulnBitfield: Long = 0L,
        version: String = "1"
    ): String {
        val v = version.take(1).ifBlank { "1" }
        val s = situationCode.take(1).ifBlank { "0" }
        val hc = headcountCode.take(1).ifBlank { "0" }
        val inj = injuryCode.take(1).ifBlank { "0" }
        val mob = mobilityCode.take(1).ifBlank { "0" }
        val urg = urgencyCode.take(1).uppercase().ifBlank { "M" }

        val needsStr = Base36.encode(needsBitfield, minLength = 3)
        val vulnStr = Base36.encode(vulnBitfield, minLength = 1)

        return "$v$s$hc$inj$mob$urg$needsStr$vulnStr".take(10)
    }

    /**
     * Encodes a canonical Q Emergency SOS frame:
     * Q|SEQ|UID|PAYLOAD_10|PACK10_GPS_10|CRC
     */
    fun encodeQFrame(
        seq: String,
        uid: String,
        situationCode: String,
        headcountCode: String,
        injuryCode: String,
        mobilityCode: String,
        urgencyCode: String,
        needsBitfield: Long,
        vulnBitfield: Long = 0L,
        latitude: Double,
        longitude: Double
    ): String {
        val safeUid = uid.trim().uppercase().replace("|", "").ifBlank { "TN01" }
        val payloadStr = encodeRequesterPayload(
            situationCode = situationCode,
            headcountCode = headcountCode,
            injuryCode = injuryCode,
            mobilityCode = mobilityCode,
            urgencyCode = urgencyCode,
            needsBitfield = needsBitfield,
            vulnBitfield = vulnBitfield
        )

        val finalLat = if (latitude != 0.0) latitude else 13.0827
        val finalLon = if (longitude != 0.0) longitude else 80.2707
        val pack10Geo = Pack10.encode(finalLat, finalLon)
        val body = "Q|$seq|$safeUid|$payloadStr|$pack10Geo"
        val checksum = xorChecksum(body)
        return "$body|$checksum"
    }

    /**
     * Converts a single resource code (e.g. 'F', 'W', 'M') into a 12-bit needs bitfield.
     */
    fun resourceCodeToBitfield(resourceCode: String): Long {
        return when (resourceCode.trim().uppercase()) {
            "F" -> 1L shl 0  // Food
            "W" -> 1L shl 1  // Water
            "M" -> 1L shl 2  // Medical Kits
            "T" -> 1L shl 3  // Tents
            "B" -> 1L shl 4  // Blankets
            "H" -> 1L shl 5  // Hygiene Kits
            "X" -> 1L shl 6  // Rescue Team
            "V" -> 1L shl 7  // Evacuation Transport
            "P" -> 1L shl 8  // Power / Generators
            "I" -> 1L shl 9  // Infant Kits
            "D" -> 1L shl 10 // Medical Team / Doctor
            "E" -> 1L shl 11 // Heavy Equipment
            else -> 1L shl 0
        }
    }

    /**
     * Encodes FieldReport to canonical N frame with PACK10 GPS coordinates and exact requested quantity.
     */
    fun encodeReport(
        report: FieldReport,
        seq: String
    ): String {
        return encodeNeed(report, seq)
    }

    fun encodeNeed(
        report: FieldReport,
        seq: String
    ): String {
        val organization = report.organizationId
            .trim()
            .uppercase()
            .replace("|", "")
            .ifBlank { "NGO01" }

        val lat: Double
        val lon: Double
        if (report.latitude != null && report.longitude != null && (report.latitude != 0.0 || report.longitude != 0.0)) {
            lat = report.latitude
            lon = report.longitude
        } else {
            val (dLat, dLon) = getCoordinatesForLocationCode(report.locationCode)
            lat = dLat
            lon = dLon
        }

        val pack10Geo = Pack10.encode(lat, lon)
        val resource = resourceCode(report.resourceCode)
        val urgency = urgencyCode(report.urgencyCode)

        val body = listOf(
            "N",
            seq,
            organization,
            pack10Geo,
            resource,
            report.quantity.toString(),
            urgency
        ).joinToString("|")

        val checksum = xorChecksum(body)
        return "$body|$checksum"
    }
}