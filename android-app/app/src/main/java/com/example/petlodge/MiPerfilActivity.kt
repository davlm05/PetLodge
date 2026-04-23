package com.example.petlodge

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.petlodge.data.ApiClient
import com.example.petlodge.data.SessionManager
import com.example.petlodge.data.dto.ApiResponse
import com.example.petlodge.data.dto.UserResponse
import com.example.petlodge.data.dto.UserUpdateRequest
import com.example.petlodge.databinding.ActivityMiPerfilBinding
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class MiPerfilActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMiPerfilBinding
    private lateinit var sessionManager: SessionManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMiPerfilBinding.inflate(layoutInflater)
        setContentView(binding.root)
        sessionManager = SessionManager(this)

        loadProfile()

        binding.btnBackToMain.setOnClickListener {
            finish()
        }

        binding.btnGuardarCambios.setOnClickListener {
            saveProfile()
        }

        binding.btnCambiarContra.setOnClickListener {
            startActivity(Intent(this, CambiarContraActivity::class.java))
        }

        binding.btnCerrarSesion.setOnClickListener {
            logout()
        }
    }

    private fun loadProfile() {
        setLoading(true)
        ApiClient.service.getProfile()
            .enqueue(object : Callback<ApiResponse<UserResponse>> {
                override fun onResponse(
                    call: Call<ApiResponse<UserResponse>>,
                    response: Response<ApiResponse<UserResponse>>
                ) {
                    setLoading(false)
                    val body = response.body()
                    val data = body?.data

                    if (response.isSuccessful && body?.success == true && data != null) {
                        populateFields(data)
                    } else {
                        Toast.makeText(
                            this@MiPerfilActivity,
                            "Error al cargar el perfil.",
                            Toast.LENGTH_SHORT
                        ).show()
                    }
                }

                override fun onFailure(call: Call<ApiResponse<UserResponse>>, t: Throwable) {
                    setLoading(false)
                    Toast.makeText(
                        this@MiPerfilActivity,
                        "Error de conexión al cargar perfil.",
                        Toast.LENGTH_SHORT
                    ).show()
                }
            })
    }

    private fun populateFields(user: UserResponse) {
        binding.etNombre.setText(user.fullName)
        binding.etCedula.setText(user.idNumber)
        binding.etCorreo.setText(user.email)
        binding.etTelefono.setText(user.phone ?: "")
        binding.etDireccion.setText(user.address ?: "")
    }

    private fun saveProfile() {
        val fullName = binding.etNombre.text.toString().trim()
        val phone = binding.etTelefono.text.toString().trim()
        val address = binding.etDireccion.text.toString().trim()

        if (fullName.isBlank()) {
            binding.etNombre.error = "El nombre es requerido."
            return
        }

        if (phone.isBlank() || phone.length < 8) {
            binding.etTelefono.error = "El numero de telefono debe tener al menos 8 caracteres"
            return
        }

        val request = UserUpdateRequest(
            fullName = fullName,
            phone = phone.ifBlank { null },
            address = address.ifBlank { null }
        )

        setLoading(true)
        ApiClient.service.updateProfile(request)
            .enqueue(object : Callback<ApiResponse<UserResponse>> {
                override fun onResponse(
                    call: Call<ApiResponse<UserResponse>>,
                    response: Response<ApiResponse<UserResponse>>
                ) {
                    setLoading(false)
                    val body = response.body()
                    if (response.isSuccessful && body?.success == true) {
                        Toast.makeText(
                            this@MiPerfilActivity,
                            "Perfil actualizado exitosamente.",
                            Toast.LENGTH_SHORT
                        ).show()
                        body.data?.let { populateFields(it) }
                    } else {
                        Toast.makeText(
                            this@MiPerfilActivity,
                            body?.error ?: "Error al actualizar el perfil.",
                            Toast.LENGTH_LONG
                        ).show()
                    }
                }

                override fun onFailure(call: Call<ApiResponse<UserResponse>>, t: Throwable) {
                    setLoading(false)
                    Toast.makeText(
                        this@MiPerfilActivity,
                        "Error de conexión al guardar cambios.",
                        Toast.LENGTH_LONG
                    ).show()
                }
            })
    }

    private fun logout() {
        sessionManager.clearSession()
        val intent = Intent(this, LoginActivity::class.java)
        intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
        startActivity(intent)
    }

    private fun setLoading(isLoading: Boolean) {
        binding.btnGuardarCambios.isEnabled = !isLoading
        binding.btnCambiarContra.isEnabled = !isLoading
        binding.btnCerrarSesion.isEnabled = !isLoading
        binding.btnGuardarCambios.text = if (isLoading) "Guardando..." else "Guardar Cambios"
    }
}
