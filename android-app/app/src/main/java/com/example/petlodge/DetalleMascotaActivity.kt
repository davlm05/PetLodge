package com.example.petlodge

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.petlodge.data.ApiClient
import com.example.petlodge.data.dto.ApiResponse
import com.example.petlodge.data.dto.PetResponse
import com.example.petlodge.databinding.ActivityDetalleMascotaBinding
import com.bumptech.glide.Glide
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class DetalleMascotaActivity : AppCompatActivity() {
    private lateinit var binding: ActivityDetalleMascotaBinding
    private var petId: Int = -1

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityDetalleMascotaBinding.inflate(layoutInflater)
        setContentView(binding.root)

        petId = intent.getIntExtra(MisMascotasActivity.EXTRA_PET_ID, -1)

        binding.btnBackToMisMascotas.setOnClickListener {
            finish()
        }

        binding.btnEditarMascota.setOnClickListener {
            if (petId <= 0) {
                Toast.makeText(this, "No se encontró la mascota.", Toast.LENGTH_LONG).show()
                return@setOnClickListener
            }

            startActivity(
                Intent(this, EditarMascotaActivity::class.java)
                    .putExtra(MisMascotasActivity.EXTRA_PET_ID, petId)
            )
        }
    }

    override fun onResume() {
        super.onResume()
        if (petId <= 0) {
            Toast.makeText(this, "No se encontró la mascota.", Toast.LENGTH_LONG).show()
            finish()
            return
        }
        loadPet()
    }

    private fun loadPet() {
        setLoading(true)
        ApiClient.service.getPetById(petId)
            .enqueue(object : Callback<ApiResponse<PetResponse>> {
                override fun onResponse(
                    call: Call<ApiResponse<PetResponse>>,
                    response: Response<ApiResponse<PetResponse>>
                ) {
                    setLoading(false)
                    val body = response.body()
                    val pet = body?.data

                    if (response.isSuccessful && body?.success == true && pet != null) {
                        renderPet(pet)
                    } else {
                        Toast.makeText(
                            this@DetalleMascotaActivity,
                            body?.error ?: "Error al cargar la mascota.",
                            Toast.LENGTH_LONG
                        ).show()
                    }
                }

                override fun onFailure(
                    call: Call<ApiResponse<PetResponse>>,
                    throwable: Throwable
                ) {
                    setLoading(false)
                    Toast.makeText(
                        this@DetalleMascotaActivity,
                        "Error al conectar con el servidor.",
                        Toast.LENGTH_LONG
                    ).show()
                }
            })
    }

    private fun renderPet(pet: PetResponse) {
        binding.tvNombre.text = pet.name
        binding.tvTipo.text = pet.species.toDisplayValue()
        binding.tvRaza.text = pet.breed.orFallback()
        binding.tvEdad.text = pet.ageYears?.toString().orFallback()
        binding.tvSexo.text = pet.sex.toDisplayValue()
        binding.tvTamano.text = pet.size.toDisplayValue()
        binding.tvVacunacionEstado.text = pet.vaccinated.toYesNo()
        binding.tvVacunacionDetalles.text = pet.vaccinationNotes.orFallback()
        binding.tvCondicionesMedicasEstado.text = pet.hasMedicalConditions.toYesNo()
        binding.tvCondicionesMedicasDetalles.text = pet.medicalConditionsNotes.orFallback()
        binding.tvVeterinarioNombre.text = pet.veterinarianName.orFallback()
        binding.tvVeterinarioTelefono.text = pet.veterinarianPhone.orFallback()
        binding.tvCuidados.text = pet.careNotes.orFallback()

        val fullUrl = ApiClient.getFullImageUrl(pet.photoUrl)
        if (fullUrl != null) {
            binding.ivMascotaFoto.setPadding(0, 0, 0, 0)
            binding.ivMascotaFoto.scaleType = android.widget.ImageView.ScaleType.CENTER_CROP
            Glide.with(this).load(fullUrl).into(binding.ivMascotaFoto)
        }
    }

    private fun String?.orFallback(): String = this?.takeIf { it.isNotBlank() } ?: "No registrado"

    private fun Boolean?.toYesNo(): String = when (this) {
        true -> "Sí"
        false -> "No"
        null -> "No registrado"
    }

    private fun String?.toDisplayValue(): String = when (this) {
        "dog" -> "Perro"
        "cat" -> "Gato"
        "bird" -> "Ave"
        "rabbit" -> "Conejo"
        "hamster" -> "Hámster"
        "reptile" -> "Reptil"
        "other" -> "Otro"
        "male" -> "Macho"
        "female" -> "Hembra"
        "small" -> "Pequeño"
        "medium" -> "Mediano"
        "large" -> "Grande"
        null -> "No registrado"
        else -> replaceFirstChar { character ->
            if (character.isLowerCase()) character.titlecase() else character.toString()
        }
    }

    private fun setLoading(isLoading: Boolean) {
        binding.progressBar.visibility = if (isLoading) View.VISIBLE else View.GONE
        binding.btnEditarMascota.isEnabled = !isLoading
    }
}
