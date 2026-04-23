package com.example.petlodge

import android.app.Application
import com.example.petlodge.data.ApiClient

class PetLodgeApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        ApiClient.initialize(this)
    }
}
