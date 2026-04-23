package com.example.petlodge.data.dto

import com.google.gson.annotations.SerializedName

data class UserResponse(
    val id: Int,
    val email: String,
    @SerializedName("full_name")
    val fullName: String,
    @SerializedName("id_number")
    val idNumber: String,
    val phone: String?,
    val address: String?,
    val role: String,
    @SerializedName("is_active")
    val isActive: Boolean,
    @SerializedName("created_at")
    val createdAt: String,
)

data class UserUpdateRequest(
    @SerializedName("full_name")
    val fullName: String,
    val phone: String?,
    val address: String?,
)

data class ChangePasswordRequest(
    @SerializedName("current_password")
    val currentPassword: String,
    @SerializedName("new_password")
    val newPassword: String,
)
