package com.example.petlodge.data.dto

import com.google.gson.annotations.SerializedName

data class NotificationResponse(
    val id: Int,
    @SerializedName("event_type")
    val eventType: String,
    val subject: String?,
    @SerializedName("recipient_email")
    val recipientEmail: String?,
    val status: String,
    @SerializedName("error_message")
    val errorMessage: String?,
    @SerializedName("sent_at")
    val sentAt: String?,
    @SerializedName("created_at")
    val createdAt: String?,
)
