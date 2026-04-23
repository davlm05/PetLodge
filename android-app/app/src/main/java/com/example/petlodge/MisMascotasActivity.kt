package com.example.petlodge

import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.widget.Button
import android.widget.ImageView
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.bumptech.glide.Glide
import com.example.petlodge.data.ApiClient
import com.example.petlodge.data.dto.ApiResponse
import com.example.petlodge.data.dto.PetResponse
import com.example.petlodge.databinding.ActivityMisMascotasBinding
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class MisMascotasActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMisMascotasBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMisMascotasBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.btnBackToMain.setOnClickListener {
            finish()
        }

        binding.btnRegistrarMascota.setOnClickListener {
            startActivity(Intent(this, RegistrarMascotaActivity::class.java))
        }
    }

    override fun onResume() {
        super.onResume()
        loadPets()
    }

    private fun loadPets() {
        setLoading(true)
        ApiClient.service.getPets()
            .enqueue(object : Callback<ApiResponse<List<PetResponse>>> {
                override fun onResponse(
                    call: Call<ApiResponse<List<PetResponse>>>,
                    response: Response<ApiResponse<List<PetResponse>>>
                ) {
                    setLoading(false)
                    val body = response.body()

                    if (response.isSuccessful && body?.success == true) {
                        renderPets(body.data.orEmpty())
                    } else {
                        renderPets(emptyList())
                        Toast.makeText(
                            this@MisMascotasActivity,
                            body?.error ?: "Error al cargar las mascotas.",
                            Toast.LENGTH_LONG
                        ).show()
                    }
                }

                override fun onFailure(
                    call: Call<ApiResponse<List<PetResponse>>>,
                    throwable: Throwable
                ) {
                    setLoading(false)
                    renderPets(emptyList())
                    Toast.makeText(
                        this@MisMascotasActivity,
                        "Error al conectar con el servidor.",
                        Toast.LENGTH_LONG
                    ).show()
                }
            })
    }

    private fun renderPets(pets: List<PetResponse>) {
        binding.petsContainer.removeAllViews()
        binding.tvEmptyState.visibility = if (pets.isEmpty()) View.VISIBLE else View.GONE

        val inflater = LayoutInflater.from(this)
        pets.forEachIndexed { index, pet ->
            val petView = inflater.inflate(
                R.layout.item_pet_card,
                binding.petsContainer,
                false
            )

            val icon = petView.findViewById<ImageView>(R.id.ivPetIcon)
            val name = petView.findViewById<TextView>(R.id.tvPetName)
            val summary = petView.findViewById<TextView>(R.id.tvPetSummary)
            val detailButton = petView.findViewById<Button>(R.id.btnViewPet)

            val fullUrl = ApiClient.getFullImageUrl(pet.photoUrl)
            if (fullUrl != null) {
                icon.clearColorFilter()
                icon.imageTintList = null
                Glide.with(this).load(fullUrl).into(icon)
            } else {
                icon.setColorFilter(
                    getColor(if (index % 2 == 0) R.color.primary else R.color.accent)
                )
            }
            name.text = pet.name
            summary.text = buildPetSummary(pet)
            detailButton.setOnClickListener {
                startActivity(
                    Intent(this, DetalleMascotaActivity::class.java)
                        .putExtra(EXTRA_PET_ID, pet.id)
                )
            }

            binding.petsContainer.addView(petView)
        }
    }

    private fun buildPetSummary(pet: PetResponse): String {
        val details = listOfNotNull(
            pet.species.toDisplayValue(),
            pet.breed?.takeIf { it.isNotBlank() },
            pet.size?.toDisplayValue()
        )
        return if (details.isEmpty()) {
            "Sin información adicional"
        } else {
            details.joinToString(" - ")
        }
    }

    private fun String.toDisplayValue(): String = when (this) {
        "dog" -> "Perro"
        "cat" -> "Gato"
        "bird" -> "Ave"
        "rabbit" -> "Conejo"
        "hamster" -> "Hámster"
        "reptile" -> "Reptil"
        "other" -> "Otro"
        "small" -> "Pequeño"
        "medium" -> "Mediano"
        "large" -> "Grande"
        else -> replaceFirstChar { character ->
            if (character.isLowerCase()) character.titlecase() else character.toString()
        }
    }

    private fun setLoading(isLoading: Boolean) {
        binding.progressBar.visibility = if (isLoading) View.VISIBLE else View.GONE
        binding.btnRegistrarMascota.isEnabled = !isLoading
    }

    companion object {
        const val EXTRA_PET_ID = "extra_pet_id"
    }
}
