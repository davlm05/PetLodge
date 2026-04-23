package com.example.petlodge.data.dto

import com.google.gson.annotations.SerializedName

data class PetRequest(
    val name: String? = null,
    val species: String? = null,
    val breed: String? = null,
    @SerializedName("age_years")
    val ageYears: Int? = null,
    val sex: String? = null,
    val size: String? = null,
    @SerializedName("photo_url")
    val photoUrl: String? = null,
    val vaccinated: Boolean? = null,
    @SerializedName("vaccination_notes")
    val vaccinationNotes: String? = null,
    @SerializedName("has_medical_conditions")
    val hasMedicalConditions: Boolean? = null,
    @SerializedName("medical_conditions_notes")
    val medicalConditionsNotes: String? = null,
    @SerializedName("veterinarian_name")
    val veterinarianName: String? = null,
    @SerializedName("veterinarian_phone")
    val veterinarianPhone: String? = null,
    @SerializedName("care_notes")
    val careNotes: String? = null,
    @SerializedName("photo_base64")
    val photoBase64: String? = null,
)

data class PetResponse(
    val id: Int,
    @SerializedName("owner_id")
    val ownerId: Int,
    val name: String,
    val species: String,
    val breed: String?,
    @SerializedName("age_years")
    val ageYears: Int?,
    val sex: String?,
    val size: String?,
    @SerializedName("photo_url")
    val photoUrl: String?,
    val vaccinated: Boolean?,
    @SerializedName("vaccination_notes")
    val vaccinationNotes: String?,
    @SerializedName("has_medical_conditions")
    val hasMedicalConditions: Boolean?,
    @SerializedName("medical_conditions_notes")
    val medicalConditionsNotes: String?,
    @SerializedName("veterinarian_name")
    val veterinarianName: String?,
    @SerializedName("veterinarian_phone")
    val veterinarianPhone: String?,
    @SerializedName("care_notes")
    val careNotes: String?,
    @SerializedName("is_deleted")
    val isDeleted: Boolean,
    @SerializedName("created_at")
    val createdAt: String,
    @SerializedName("updated_at")
    val updatedAt: String,
)
