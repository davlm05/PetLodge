package com.example.petlodge.data

import android.content.Context
import com.google.gson.GsonBuilder
import okhttp3.Interceptor
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

object ApiClient {
    const val SERVER_IP = "10.0.2.2"
    // Default: 10.0.2.2

    const val BASE_URL = "http://$SERVER_IP:5000/api/v1/"
    private const val STATIC_URL = "http://$SERVER_IP:5000"

    fun getFullImageUrl(url: String?): String? {
        if (url.isNullOrBlank()) return null
        return if (url.startsWith("http")) url else "$STATIC_URL$url"
    }

    private var appContext: Context? = null
    private val gson = GsonBuilder()
        .serializeNulls()
        .create()

    private val loggingInterceptor = HttpLoggingInterceptor().apply {
        level = HttpLoggingInterceptor.Level.BASIC
    }

    private val authInterceptor = Interceptor { chain ->
        val token = appContext?.let { SessionManager(it).getAccessToken() }
        val request = chain.request().newBuilder().apply {
            if (!token.isNullOrBlank()) {
                header("Authorization", "Bearer $token")
            }
        }.build()

        chain.proceed(request)
    }

    fun initialize(context: Context) {
        appContext = context.applicationContext
    }

    private val okHttpClient = OkHttpClient.Builder()
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .writeTimeout(30, TimeUnit.SECONDS)
        .addInterceptor(authInterceptor)
        .addInterceptor(loggingInterceptor)
        .build()

    private val retrofit = Retrofit.Builder()
        .baseUrl(BASE_URL)
        .client(okHttpClient)
        .addConverterFactory(GsonConverterFactory.create(gson))
        .build()

    val service: PetLodgeApiService = retrofit.create(PetLodgeApiService::class.java)
}
