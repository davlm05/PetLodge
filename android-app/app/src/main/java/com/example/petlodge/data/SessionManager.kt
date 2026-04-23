package com.example.petlodge.data

import android.content.Context

class SessionManager(context: Context) {
    private val preferences = context.getSharedPreferences(PREFERENCES_NAME, Context.MODE_PRIVATE)

    fun saveSession(accessToken: String, refreshToken: String, userId: Int, fullName: String, email: String, role: String) {
        preferences.edit()
            .putString(KEY_ACCESS_TOKEN, accessToken)
            .putString(KEY_REFRESH_TOKEN, refreshToken)
            .putInt(KEY_USER_ID, userId)
            .putString(KEY_FULL_NAME, fullName)
            .putString(KEY_EMAIL, email)
            .putString(KEY_ROLE, role)
            .apply()
    }

    fun getAccessToken(): String? = preferences.getString(KEY_ACCESS_TOKEN, null)
    fun getFullName(): String? = preferences.getString(KEY_FULL_NAME, null)
    fun getEmail(): String? = preferences.getString(KEY_EMAIL, null)
    fun getUserId(): Int = preferences.getInt(KEY_USER_ID, -1)

    fun clearSession() {
        preferences.edit().clear().apply()
    }

    companion object {
        private const val PREFERENCES_NAME = "petlodge_session"
        private const val KEY_ACCESS_TOKEN = "access_token"
        private const val KEY_REFRESH_TOKEN = "refresh_token"
        private const val KEY_USER_ID = "user_id"
        private const val KEY_FULL_NAME = "full_name"
        private const val KEY_EMAIL = "email"
        private const val KEY_ROLE = "role"
    }
}

