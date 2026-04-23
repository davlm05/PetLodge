package com.example.petlodge.data.dto

import com.google.gson.annotations.SerializedName

data class RoomResponse(
    val id: Int,
    val number: String,
    val name: String,
    @SerializedName("room_type")
    val roomType: String,
    val capacity: Int?,
    @SerializedName("price_per_night")
    val pricePerNight: Double,
    val description: String?,
    @SerializedName("is_active")
    val isActive: Boolean,
)

data class ServiceResponse(
    val id: Int,
    val name: String,
    val description: String?,
    val price: Double,
    @SerializedName("is_active")
    val isActive: Boolean,
)
