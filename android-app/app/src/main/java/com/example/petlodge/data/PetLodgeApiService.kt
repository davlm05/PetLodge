package com.example.petlodge.data

import com.example.petlodge.data.dto.ApiResponse
import com.example.petlodge.data.dto.ChangePasswordRequest
import com.example.petlodge.data.dto.LoginRequest
import com.example.petlodge.data.dto.LoginResponse
import com.example.petlodge.data.dto.NotificationResponse
import com.example.petlodge.data.dto.PetRequest
import com.example.petlodge.data.dto.PetResponse
import com.example.petlodge.data.dto.RegisterRequest
import com.example.petlodge.data.dto.ReservationCreateRequest
import com.example.petlodge.data.dto.ReservationResponse
import com.example.petlodge.data.dto.RoomResponse
import com.example.petlodge.data.dto.ServiceResponse
import com.example.petlodge.data.dto.UserResponse
import com.example.petlodge.data.dto.UserUpdateRequest
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.DELETE
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.PUT
import retrofit2.http.Path

interface PetLodgeApiService {

    // Auth
    @POST("auth/login")
    fun login(@Body request: LoginRequest): Call<ApiResponse<LoginResponse>>

    @POST("auth/register")
    fun register(@Body request: RegisterRequest): Call<ApiResponse<UserResponse>>

    @PUT("auth/change-password")
    fun changePassword(@Body request: ChangePasswordRequest): Call<ApiResponse<Unit>>

    // Users / Profile
    @GET("users/me")
    fun getProfile(): Call<ApiResponse<UserResponse>>

    @PUT("users/me")
    fun updateProfile(@Body request: UserUpdateRequest): Call<ApiResponse<UserResponse>>

    // Pets
    @GET("pets/")
    fun getPets(): Call<ApiResponse<List<PetResponse>>>

    @POST("pets/")
    fun createPet(@Body request: PetRequest): Call<ApiResponse<PetResponse>>

    @GET("pets/{petId}")
    fun getPetById(@Path("petId") petId: Int): Call<ApiResponse<PetResponse>>

    @PUT("pets/{petId}")
    fun updatePet(
        @Path("petId") petId: Int,
        @Body request: PetRequest
    ): Call<ApiResponse<PetResponse>>

    @DELETE("pets/{petId}")
    fun deletePet(@Path("petId") petId: Int): Call<ApiResponse<Unit>>

    // Catalog
    @GET("rooms")
    fun getRooms(): Call<ApiResponse<List<RoomResponse>>>

    @GET("services")
    fun getServices(): Call<ApiResponse<List<ServiceResponse>>>

    // Reservations
    @GET("reservations/")
    fun getReservations(): Call<ApiResponse<List<ReservationResponse>>>

    @POST("reservations/")
    fun createReservation(
        @Body request: ReservationCreateRequest
    ): Call<ApiResponse<ReservationResponse>>

    @DELETE("reservations/{reservationId}")
    fun cancelReservation(
        @Path("reservationId") reservationId: Int
    ): Call<ApiResponse<ReservationResponse>>

    // Notifications
    @GET("notifications/")
    fun getNotifications(): Call<ApiResponse<List<NotificationResponse>>>
}

