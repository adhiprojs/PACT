package org.humanitarian.fieldapp.sms

/**
 * Base-36 encoding and decoding utilities matching the PACT Python backend.
 * Alphabet: 0-9, A-Z (radix 36).
 */
object Base36 {

    private const val ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    private val CHAR_MAP = ALPHABET.mapIndexed { index, char -> char to index.toLong() }.toMap()

    fun encode(number: Long, minLength: Int = 0): String {
        if (number < 0) {
            throw IllegalArgumentException("Cannot encode negative integer $number in base36")
        }
        if (number == 0L) {
            return "0".padStart(minLength, '0')
        }

        val chars = StringBuilder()
        var n = number
        while (n > 0) {
            val rem = (n % 36).toInt()
            chars.append(ALPHABET[rem])
            n /= 36
        }

        val encoded = chars.reverse().toString()
        return if (minLength > 0 && encoded.length < minLength) {
            encoded.padStart(minLength, '0')
        } else {
            encoded
        }
    }

    fun decode(s: String): Long {
        val trimmed = s.trim().uppercase()
        if (trimmed.isEmpty()) {
            throw IllegalArgumentException("Cannot decode empty string in base36")
        }
        var value = 0L
        for (char in trimmed) {
            val digit = CHAR_MAP[char] ?: throw IllegalArgumentException("Invalid Base-36 character '$char' in '$s'")
            value = value * 36 + digit
        }
        return value
    }
}
