package org.humanitarian.fieldapp.models

import android.content.Context
import android.content.SharedPreferences

data class UserProfile(
    val roleKey: String,          // "admin", "donor", "individual"
    val roleTitle: String,        // "Administrator", "Donor Group", "Individual"
    val displayName: String,      // "Adhi"
    val organizationId: String    // "RADM12"
)

object UserSession {
    private const val PREFS_NAME = "pact_user_session"
    private const val KEY_LOGGED_IN = "is_logged_in"
    private const val KEY_ROLE_KEY = "role_key"
    private const val KEY_ROLE_TITLE = "role_title"
    private const val KEY_DISPLAY_NAME = "display_name"
    private const val KEY_ORG_ID = "org_id"

    private fun getPrefs(context: Context): SharedPreferences {
        return context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
    }

    fun isLoggedIn(context: Context): Boolean {
        return getPrefs(context).getBoolean(KEY_LOGGED_IN, false)
    }

    fun getUser(context: Context): UserProfile {
        val prefs = getPrefs(context)
        return UserProfile(
            roleKey = prefs.getString(KEY_ROLE_KEY, "individual") ?: "individual",
            roleTitle = prefs.getString(KEY_ROLE_TITLE, "Individual") ?: "Individual",
            displayName = prefs.getString(KEY_DISPLAY_NAME, "Worker") ?: "Worker",
            organizationId = prefs.getString(KEY_ORG_ID, "IND01") ?: "IND01"
        )
    }

    fun saveUser(context: Context, profile: UserProfile) {
        getPrefs(context).edit()
            .putBoolean(KEY_LOGGED_IN, true)
            .putString(KEY_ROLE_KEY, profile.roleKey)
            .putString(KEY_ROLE_TITLE, profile.roleTitle)
            .putString(KEY_DISPLAY_NAME, profile.displayName)
            .putString(KEY_ORG_ID, profile.organizationId)
            .apply()
    }

    fun logout(context: Context) {
        getPrefs(context).edit().clear().apply()
    }
}
