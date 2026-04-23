package com.example.petlodge

import android.content.Intent
import android.os.Bundle
import android.util.Patterns
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.petlodge.data.ApiClient
import com.example.petlodge.data.SessionManager
import com.example.petlodge.data.dto.ApiResponse
import com.example.petlodge.data.dto.LoginRequest
import com.example.petlodge.data.dto.LoginResponse
import com.example.petlodge.databinding.ActivityLoginBinding
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class LoginActivity : AppCompatActivity() {
    private lateinit var binding: ActivityLoginBinding
    private lateinit var sessionManager: SessionManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityLoginBinding.inflate(layoutInflater)
        setContentView(binding.root)
        sessionManager = SessionManager(this)

        binding.btnNavigateToMain.setOnClickListener {
            login()
        }

        binding.btnNavigateToRegister.setOnClickListener {
            startActivity(Intent(this, RegisterActivity::class.java))
        }
    }

    private fun login() {
        val email = binding.etEmail.text.toString().trim()
        val password = binding.etPassword.text.toString()

        if (!validateFields(email, password)) return

        setLoading(true)
        ApiClient.service.login(LoginRequest(email, password))
            .enqueue(object : Callback<ApiResponse<LoginResponse>> {
                override fun onResponse(
                    call: Call<ApiResponse<LoginResponse>>,
                    response: Response<ApiResponse<LoginResponse>>
                ) {
                    setLoading(false)
                    val body = response.body()
                    val data = body?.data

                    if (response.isSuccessful && body?.success == true && data != null) {
                        sessionManager.saveSession(
                            accessToken = data.accessToken,
                            refreshToken = data.refreshToken,
                            userId = data.user.id,
                            fullName = data.user.fullName,
                            email = data.user.email,
                            role = data.user.role,
                        )
                        startActivity(Intent(this@LoginActivity, MainActivity::class.java))
                        finish()
                    } else {
                        Toast.makeText(
                            this@LoginActivity,
                            body?.error ?: "Error al iniciar sesion.",
                            Toast.LENGTH_LONG
                        ).show()
                    }
                }

                override fun onFailure(call: Call<ApiResponse<LoginResponse>>, throwable: Throwable) {
                    setLoading(false)
                    Toast.makeText(
                        this@LoginActivity,
                        "Error al conectar con el servidor.",
                        Toast.LENGTH_LONG
                    ).show()
                }
            })
    }

    private fun validateFields(email: String, password: String): Boolean {
        if (email.isBlank()) {
            binding.etEmail.error = "Ingresa tu correo."
            return false
        }

        if (!Patterns.EMAIL_ADDRESS.matcher(email).matches()) {
            binding.etEmail.error = "Ingresa un correo valido."
            return false
        }

        if (password.isBlank()) {
            binding.etPassword.error = "Ingresa tu contrasena."
            return false
        }

        return true
    }

    private fun setLoading(isLoading: Boolean) {
        binding.btnNavigateToMain.isEnabled = !isLoading
        binding.btnNavigateToRegister.isEnabled = !isLoading
        binding.btnNavigateToMain.text = if (isLoading) "Iniciando..." else "Iniciar Sesion"
    }
}
