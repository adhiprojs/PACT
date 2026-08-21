package org.humanitarian.fieldapp.sms

private val validLocationCodes = setOf(
    "RA",
    "RB",
    "RC",
    "D1",
    "D2"
)

private val validResourceCodes = setOf(
    "F",
    "W",
    "M",
    "T",
    "B",
    "H",
    "D",
    "U"
)

private val validUrgencyCodes = setOf(
    "L",
    "M",
    "H",
    "C"
)

/**
 * Maps location codes to default Tamil Nadu disaster coordinates when GPS is not yet acquired.
 */
fun getCoordinatesForLocationCode(code: String): Pair<Double, Double> {
    return when (code.trim().uppercase()) {
        "RA", "REGION A" -> Pair(13.0827, 80.2707)       // Chennai Central
        "RB", "REGION B" -> Pair(11.7480, 79.7714)       // Cuddalore Coastal Delta
        "RC", "REGION C" -> Pair(9.9252, 78.1198)        // Madurai South Hub
        "D1", "DISTRICT NORTH" -> Pair(13.2300, 80.3100) // Ennore / Tiruvallur Basin
        "D2", "DISTRICT SOUTH" -> Pair(12.9249, 80.1000) // Tambaram / Chengalpattu
        else -> Pair(13.0827, 80.2707)
    }
}

fun locationCode(value: String): String {
    val cleaned = value.trim().uppercase()

    return when {
        cleaned in validLocationCodes -> cleaned
        cleaned == "REGION A" -> "RA"
        cleaned == "REGION B" -> "RB"
        cleaned == "REGION C" -> "RC"
        cleaned == "DISTRICT NORTH" -> "D1"
        cleaned == "DISTRICT SOUTH" -> "D2"
        else -> cleaned.take(8).ifBlank { "RA" }
    }
}

fun resourceCode(value: String): String {
    val cleaned = value.trim().uppercase()

    return when {
        cleaned in validResourceCodes -> cleaned
        cleaned == "FOOD" || cleaned == "FOOD KITS" || cleaned == "FOOD_KITS" -> "F"
        cleaned == "WATER" || cleaned == "WATER KITS" || cleaned == "WATER_KITS" -> "W"
        cleaned == "MEDICAL" || cleaned == "MEDICAL KITS" || cleaned == "MEDICAL_KITS" -> "M"
        cleaned == "TENTS" || cleaned == "TENT" -> "T"
        cleaned == "BLANKETS" || cleaned == "BLANKET" -> "B"
        cleaned == "HYGIENE" || cleaned == "HYGIENE KITS" || cleaned == "HYGIENE_KITS" -> "H"
        cleaned == "MEDICAL TEAMS" || cleaned == "MEDICAL_TEAMS" -> "D"
        cleaned == "UNKNOWN" -> "U"
        else -> "U"
    }
}

fun urgencyCode(value: String): String {
    val cleaned = value.trim().uppercase()

    return when {
        cleaned in validUrgencyCodes -> cleaned
        cleaned == "LOW" -> "L"
        cleaned == "MEDIUM" -> "M"
        cleaned == "HIGH" -> "H"
        cleaned == "CRITICAL" -> "C"
        else -> "M"
    }
}