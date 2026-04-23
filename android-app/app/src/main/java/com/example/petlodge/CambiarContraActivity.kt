package com.example.petlodge

import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.petlodge.data.ApiClient
import com.example.petlodge.data.dto.ApiResponse
import com.example.petlodge.data.dto.ChangePasswordRequest
import com.example.petlodge.databinding.ActivityCambiarContraBinding
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class CambiarContraActivity : AppCompatActivity() {
    private lateinit var binding: ActivityCambiarContraBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityCambiarContraBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.btnBackToProfile.setOnClickListener {
            finish()
        }

        binding.btnSave.setOnClickListener {
            changePassword()
        }
    }

    private fun changePassword() {
        val currentPassword = binding.etCurrentPassword.text.toString()
        val newPassword = binding.etNewPassword.text.toString()
        val confirmPassword = binding.etConfirmNewPassword.text.toString()

        if (!validateFields(currentPassword, newPassword, confirmPassword)) return

        val request = ChangePasswordRequest(
            currentPassword = currentPassword,
            newPassword = newPassword
        )

        setLoading(true)
        ApiClient.service.changePassword(request)
            .enqueue(object : Callback<ApiResponse<Unit>> {
                override fun onResponse(
                    call: Call<ApiResponse<Unit>>,
                    response: Response<ApiResponse<Unit>>
                ) {
                    setLoading(false)
                    val body = response.body()
                    if (response.isSuccessful && body?.success == true) {
                        Toast.makeText(
                            this@CambiarContraActivity,
                            "Contraseña actualizada exitosamente.",
                            Toast.LENGTH_SHORT
                        ).show()
                        finish()
                    } else {
                        Toast.makeText(
                            this@CambiarContraActivity,
                            body?.error ?: "Error al cambiar la contraseña.",
                            Toast.LENGTH_LONG
                        ).show()
                    }
                }

                override fun onFailure(call: Call<ApiResponse<Unit>>, t: Throwable) {
                    setLoading(false)
                    Toast.makeText(
                        this@CambiarContraActivity,
                        "Error de conexión. Intenta de nuevo.",
                        Toast.LENGTH_LONG
                    ).show()
                }
            })
    }

    private fun validateFields(current: String, new: String, confirm: String): Boolean {
        if (current.isBlank()) {
            binding.etCurrentPassword.error = "Ingresa tu contraseña actual."
            return false
        }
        if (new.isBlank()) {
            binding.etNewPassword.error = "Ingresa la nueva contraseña."
            return false
        }
        if (new.length < 8) {
            binding.etNewPassword.error = "La contraseña debe tener al menos 8 caracteres."
            return false
        }
        if (new != confirm) {
            binding.etConfirmNewPassword.error = "Las contraseñas no coinciden."
            return false
        }
        return true
    }

    private fun setLoading(isLoading: Boolean) {
        binding.btnSave.isEnabled = !isLoading
        binding.btnSave.text = if (isLoading) "Actualizando..." else "Actualizar Contraseña"
    }
}
