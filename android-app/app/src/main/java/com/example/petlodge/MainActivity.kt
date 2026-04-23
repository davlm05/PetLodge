package com.example.petlodge

import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.example.petlodge.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.btnMisMascotas.setOnClickListener {
            startActivity(Intent(this, MisMascotasActivity::class.java))
        }
        binding.btnMisReservas.setOnClickListener {
            startActivity(Intent(this, MisReservasActivity::class.java))
        }
        binding.btnCrearReserva.setOnClickListener {
            startActivity(Intent(this, CrearReservaActivity::class.java))
        }
        binding.btnNotificaciones.setOnClickListener {
            startActivity(Intent(this, NotificacionesActivity::class.java))
        }
        binding.btnPerfil.setOnClickListener {
            startActivity(Intent(this, MiPerfilActivity::class.java))
        }
    }
}
