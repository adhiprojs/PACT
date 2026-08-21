package org.humanitarian.fieldapp.sms

import android.content.Context
import android.os.Build
import android.telephony.SmsManager
import android.util.Log

object DirectSmsSender {

    private const val TAG = "DirectSmsSender"

    /**
     * Sends an SMS silently in the background directly via Cellular SIM.
     * Does NOT open the external SMS messenger app.
     */
    fun sendDirectSms(context: Context, phoneNumber: String, message: String): Boolean {
        return try {
            val smsManager: SmsManager = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                context.getSystemService(SmsManager::class.java) ?: SmsManager.getDefault()
            } else {
                @Suppress("DEPRECATION")
                SmsManager.getDefault()
            }

            if (message.length > 160) {
                val parts = smsManager.divideMessage(message)
                smsManager.sendMultipartTextMessage(phoneNumber, null, parts, null, null)
            } else {
                smsManager.sendTextMessage(phoneNumber, null, message, null, null)
            }

            Log.i(TAG, "Successfully dispatched direct background SMS to $phoneNumber: $message")
            true
        } catch (e: Exception) {
            Log.e(TAG, "Failed to send background SMS to $phoneNumber", e)
            false
        }
    }
}
