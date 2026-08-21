package org.humanitarian.fieldapp.sms

import kotlin.math.roundToLong

/**
 * PACK10 Geolocation Codec matching PACT Python specification.
 * Encodes GPS latitude/longitude into a 10-character Base-36 string with ~1.1m precision.
 */
object Pack10 {

    data class GeoDecoded(
        val latitude: Double,
        val longitude: Double,
        val accuracyMeters: Int = 5
    )

    fun encode(lat: Double, lon: Double): String {
        val clampedLat = lat.coerceIn(-90.0, 90.0)
        val clampedLon = lon.coerceIn(-180.0, 180.0)

        val latOffset = ((clampedLat + 90.0) * 100000.0).roundToLong()
        val lonOffset = ((clampedLon + 180.0) * 100000.0).roundToLong()

        val latToken = Base36.encode(latOffset, minLength = 5)
        val lonToken = Base36.encode(lonOffset, minLength = 5)

        return latToken + lonToken
    }

    fun decode(pack10Str: String): GeoDecoded {
        val s = pack10Str.trim().uppercase()
        if (s.length < 10) {
            throw IllegalArgumentException("PACK10 string must be at least 10 characters: '$pack10Str'")
        }

        val latToken = s.substring(0, 5)
        val lonToken = s.substring(5, 10)

        val latOffset = Base36.decode(latToken)
        val lonOffset = Base36.decode(lonToken)

        val lat = (latOffset / 100000.0) - 90.0
        val lon = (lonOffset / 100000.0) - 180.0

        val roundedLat = (lat * 100000.0).roundToLong() / 100000.0
        val roundedLon = (lon * 100000.0).roundToLong() / 100000.0

        return GeoDecoded(
            latitude = roundedLat,
            longitude = roundedLon,
            accuracyMeters = 5
        )
    }
}
