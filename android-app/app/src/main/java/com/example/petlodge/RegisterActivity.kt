package com.example.petlodge

import android.content.Intent
import android.os.Bundle
import android.util.Patterns
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.petlodge.data.ApiClient
import com.example.petlodge.data.dto.ApiResponse
import com.example.petlodge.data.dto.RegisterRequest
import com.example.petlodge.data.dto.UserResponse
import com.example.petlodge.databinding.ActivityRegisterBinding
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class RegisterActivity : AppCompatActivity() {
    private lateinit var binding: ActivityRegisterBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityRegisterBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.btnBackToLogin.setOnClickListener {
            finish()
        }

        binding.btnNavigateToLogin.setOnClickListener {
            register()
        }
    }

    private fun register() {
        val fullName   = binding.etNombre.text.toString().trim()
        val idNumber   = binding.etCedula.text.toString().trim()
        val email      = binding.etEmail.text.toString().trim()
        val phone      = binding.etTelefono.text.toString().trim()
        val address    = binding.etDireccion.text.toString().trim()
        val password   = binding.etPassword.text.toString()
        val confirm    = binding.etConfirmPassword.text.toString()

        if (!validateFields(fullName, idNumber, email, phone, password, confirm)) return

        val request = RegisterRequest(
            email    = email,
            password = password,
            fullName = fullName,
            idNumber = idNumber,
            phone    = phone.ifBlank { null },
            address  = address.ifBlank { null },
        )

        setLoading(true)
        ApiClient.service.register(request)
            .enqueue(object : Callback<ApiResponse<UserResponse>> {
                override fun onResponse(
                    call: Call<ApiResponse<UserResponse>>,
                    response: Response<ApiResponse<UserResponse>>
                ) {
                    setLoading(false)
                    val body = response.body()

                    if (response.isSuccessful && body?.success == true) {
                        Toast.makeText(
                            this@RegisterActivity,
                            "¡Cuenta creada exitosamente! Inicia sesión.",
                            Toast.LENGTH_LONG
                        ).show()
                        // Ir al login y limpiar el back stack
                        val intent = Intent(this@RegisterActivity, LoginActivity::class.java)
                        intent.flags = Intent.FLAG_ACTIVITY_CLEAR_TOP or Intent.FLAG_ACTIVITY_SINGLE_TOP
                        startActivity(intent)
                        finish()
                    } else {
                        val errMsg = when (body?.code) {
                            "EMAIL_EXISTS"   -> "El correo electrónico ya está registrado."
                            "ID_EXISTS"      -> "El número de cédula ya está registrado."
                            else             -> body?.error ?: "No se pudo crear la cuenta."
                        }
                        Toast.makeText(this@RegisterActivity, errMsg, Toast.LENGTH_LONG).show()
                    }
                }

                override fun onFailure(call: Call<ApiResponse<UserResponse>>, t: Throwable) {
                    setLoading(false)
                    Toast.makeText(
                        this@RegisterActivity,
                        "Error de conexión. Intenta de nuevo.",
                        Toast.LENGTH_LONG
                    ).show()
                }
            })
    }

    private fun validateFields(
        fullName: String,
        idNumber: String,
        email: String,
        phone: String,
        password: String,
        confirm: String
    ): Boolean {
        if (fullName.isBlank()) {
            binding.etNombre.error = "El nombre es requerido."
            binding.etNombre.requestFocus()
            return false
        }
        if (idNumber.isBlank() || idNumber.length < 8) {
            binding.etCedula.error = "La cédula debe tener al menos 8 caracteres."
            binding.etCedula.requestFocus()
            return false
        }
        if (email.isBlank()) {
            binding.etEmail.error = "El correo es requerido."
            binding.etEmail.requestFocus()
            return false
        }
        if (!Patterns.EMAIL_ADDRESS.matcher(email).matches()) {
            binding.etEmail.error = "Ingresa un correo válido."
            binding.etEmail.requestFocus()
            return false
        }
        if (phone.isBlank() || phone.length < 8) {
            binding.etTelefono.error = "El teléfono es requerido."
            binding.etTelefono.requestFocus()
            return false
        }
        if (password.isBlank()) {
            binding.etPassword.error = "La contraseña es requerida."
            binding.etPassword.requestFocus()
            return false
        }
        if (password.length < 8) {
            binding.etPassword.error = "La contraseña debe tener al menos 8 caracteres."
            binding.etPassword.requestFocus()
            return false
        }
        if (password != confirm) {
            binding.etConfirmPassword.error = "Las contraseñas no coinciden."
            binding.etConfirmPassword.requestFocus()
            return false
        }
        return true
    }

    private fun setLoading(isLoading: Boolean) {
        binding.btnNavigateToLogin.isEnabled = !isLoading
        binding.btnNavigateToLogin.text = if (isLoading) "Creando cuenta..." else "Crear Cuenta"
    }
}
