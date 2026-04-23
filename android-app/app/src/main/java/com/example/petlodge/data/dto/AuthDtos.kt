package com.example.petlodge.data.dto

import com.google.gson.annotations.SerializedName

data class ApiResponse<T>(
    val success: Boolean,
    val message: String?,
    val data: T?,
    val error: String?,
    val code: String?
)

data class LoginRequest(
    val email: String,
    val password: String
)

data class LoginResponse(
    @SerializedName("access_token")
    val accessToken: String,
    @SerializedName("refresh_token")
    val refreshToken: String,
    val user: AuthUser
)

data class AuthUser(
    val id: Int,
    val email: String,
    @SerializedName("full_name")
    val fullName: String,
    val role: String
)

data class RegisterRequest(
    val email: String,
    val password: String,
    @SerializedName("full_name")
    val fullName: String,
    @SerializedName("id_number")
    val idNumber: String,
    val phone: String?,
    val address: String?,
)

