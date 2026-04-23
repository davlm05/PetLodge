package com.example.petlodge.data.dto

import com.google.gson.annotations.SerializedName

data class ReservationCreateRequest(
    @SerializedName("pet_id")
    val petId: Int,
    @SerializedName("room_id")
    val roomId: Int,
    @SerializedName("check_in_date")
    val checkInDate: String,
    @SerializedName("check_out_date")
    val checkOutDate: String,
    @SerializedName("lodging_type")
    val lodgingType: String,
    val notes: String? = null,
    @SerializedName("service_ids")
    val serviceIds: List<Int> = emptyList(),
)

data class ReservationResponse(
    val id: Int,
    @SerializedName("owner_id")
    val ownerId: Int?,
    @SerializedName("pet_id")
    val petId: Int,
    @SerializedName("room_id")
    val roomId: Int,
    val pet: ReservationPet?,
    val room: ReservationRoom?,
    @SerializedName("check_in_date")
    val checkInDate: String,
    @SerializedName("check_out_date")
    val checkOutDate: String,
    @SerializedName("lodging_type")
    val lodgingType: String,
    val status: String,
    @SerializedName("total_price")
    val totalPrice: Double?,
    val notes: String?,
    val services: List<ReservationServiceItem>?,
    @SerializedName("created_at")
    val createdAt: String?,
    @SerializedName("updated_at")
    val updatedAt: String?,
)

data class ReservationPet(
    val id: Int,
    val name: String,
)

data class ReservationRoom(
    val id: Int,
    val number: String,
)

data class ReservationServiceItem(
    val id: Int,
    @SerializedName("service_id")
    val serviceId: Int,
    @SerializedName("service_name")
    val serviceName: String?,
    val quantity: Int,
    val subtotal: Double,
)
