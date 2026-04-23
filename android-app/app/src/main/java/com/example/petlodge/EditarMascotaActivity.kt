package com.example.petlodge

import android.content.Intent
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.petlodge.data.ApiClient
import com.example.petlodge.data.dto.ApiResponse
import com.example.petlodge.data.dto.PetRequest
import com.example.petlodge.data.dto.PetResponse
import com.example.petlodge.databinding.ActivityEditarMascotaBinding
import android.net.Uri
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.util.Base64
import android.view.View
import androidx.activity.result.contract.ActivityResultContracts
import java.io.ByteArrayOutputStream
import com.bumptech.glide.Glide
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class EditarMascotaActivity : AppCompatActivity() {
    private lateinit var binding: ActivityEditarMascotaBinding
    private var petId: Int = -1
    private var photoBase64String: String? = null

    private val pickImageLauncher = registerForActivityResult(ActivityResultContracts.GetContent()) { uri: Uri? ->
        uri?.let { processImage(it) }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityEditarMascotaBinding.inflate(layoutInflater)
        setContentView(binding.root)

        petId = intent.getIntExtra(MisMascotasActivity.EXTRA_PET_ID, -1)

        binding.btnBackToDetalle.setOnClickListener {
            finish()
        }

        binding.btnSeleccionarImagen.setOnClickListener {
            pickImageLauncher.launch("image/*")
        }

        binding.btnSave.setOnClickListener {
            updatePet()
        }

        binding.btnDelete.setOnClickListener {
            deletePet()
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
                        populateForm(pet)
                    } else {
                        Toast.makeText(
                            this@EditarMascotaActivity,
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
                        this@EditarMascotaActivity,
                        "Error al conectar con el servidor.",
                        Toast.LENGTH_LONG
                    ).show()
                }
            })
    }

    private fun populateForm(pet: PetResponse) {
        binding.etNombre.setText(pet.name)
        binding.etTipo.setText(pet.species.toSpanishValue())
        binding.etRaza.setText(pet.breed.orEmpty())
        binding.etEdad.setText(pet.ageYears?.toString().orEmpty())
        binding.etSexo.setText(pet.sex.toSpanishValue())
        binding.etTamano.setText(pet.size.toSpanishValue())
        binding.etVacunacionEstado.setText(pet.vaccinated.toYesNoInput())
        binding.etVacunacionDetalles.setText(pet.vaccinationNotes.orEmpty())
        binding.etCondicionesMedicasEstado.setText(pet.hasMedicalConditions.toYesNoInput())
        binding.etCondicionesMedicasDetalles.setText(pet.medicalConditionsNotes.orEmpty())
        binding.etNombreVet.setText(pet.veterinarianName.orEmpty())
        binding.etTelefonoVet.setText(pet.veterinarianPhone.orEmpty())

        val careSections = splitCareNotes(pet.careNotes)
        binding.etCuidadosEspeciales.setText(careSections.first)
        binding.etAlimentacion.setText(careSections.second)

        val fullUrl = ApiClient.getFullImageUrl(pet.photoUrl)
        if (fullUrl != null) {
            binding.ivPreviewImage.visibility = View.VISIBLE
            Glide.with(this).load(fullUrl).into(binding.ivPreviewImage)
        }
    }

    private fun updatePet() {
        val name = binding.etNombre.text.toString().trim()
        val species = mapSpecies(binding.etTipo.text.toString())
        val breed = binding.etRaza.text.toString().trim().ifBlank { null }
        val ageYears = binding.etEdad.text.toString().trim().toIntOrNull()
        val sex = mapSex(binding.etSexo.text.toString())
        val size = mapSize(binding.etTamano.text.toString())
        val vaccinated = parseBooleanField(binding.etVacunacionEstado.text.toString())
        val vaccinationNotes = binding.etVacunacionDetalles.text.toString().trim().ifBlank { null }
        val hasMedicalConditions = parseBooleanField(
            binding.etCondicionesMedicasEstado.text.toString()
        )
        val medicalConditionsNotes =
            binding.etCondicionesMedicasDetalles.text.toString().trim().ifBlank { null }
        val veterinarianName = binding.etNombreVet.text.toString().trim().ifBlank { null }
        val veterinarianPhone = binding.etTelefonoVet.text.toString().trim().ifBlank { null }
        val careNotes = buildCareNotes(
            binding.etCuidadosEspeciales.text.toString().trim(),
            binding.etAlimentacion.text.toString().trim()
        )

        if (!validateFields(
                name = name,
                rawSpecies = binding.etTipo.text.toString(),
                species = species,
                rawSex = binding.etSexo.text.toString(),
                sex = sex,
                rawSize = binding.etTamano.text.toString(),
                size = size,
                rawVaccinated = binding.etVacunacionEstado.text.toString(),
                vaccinated = vaccinated,
                vaccinationNotes = vaccinationNotes,
                rawHasMedicalConditions = binding.etCondicionesMedicasEstado.text.toString(),
                hasMedicalConditions = hasMedicalConditions,
                medicalConditionsNotes = medicalConditionsNotes,
                rawAge = binding.etEdad.text.toString()
            )
        ) {
            return
        }

        val request = PetRequest(
            name = name,
            species = species,
            breed = breed,
            ageYears = ageYears,
            sex = sex,
            size = size,
            vaccinated = vaccinated,
            vaccinationNotes = vaccinationNotes,
            hasMedicalConditions = hasMedicalConditions,
            medicalConditionsNotes = medicalConditionsNotes,
            veterinarianName = veterinarianName,
            veterinarianPhone = veterinarianPhone,
            careNotes = careNotes,
            photoBase64 = photoBase64String
        )

        setLoading(true)
        ApiClient.service.updatePet(petId, request)
            .enqueue(object : Callback<ApiResponse<PetResponse>> {
                override fun onResponse(
                    call: Call<ApiResponse<PetResponse>>,
                    response: Response<ApiResponse<PetResponse>>
                ) {
                    setLoading(false)
                    val body = response.body()

                    if (response.isSuccessful && body?.success == true) {
                        Toast.makeText(
                            this@EditarMascotaActivity,
                            body.message ?: "Mascota actualizada exitosamente.",
                            Toast.LENGTH_LONG
                        ).show()
                        finish()
                    } else {
                        Toast.makeText(
                            this@EditarMascotaActivity,
                            body?.error ?: "Error al actualizar la mascota.",
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
                        this@EditarMascotaActivity,
                        "Error al conectar con el servidor.",
                        Toast.LENGTH_LONG
                    ).show()
                }
            })
    }

    private fun deletePet() {
        if (petId <= 0) {
            Toast.makeText(this, "No se encontró la mascota.", Toast.LENGTH_LONG).show()
            return
        }

        setLoading(true)
        ApiClient.service.deletePet(petId)
            .enqueue(object : Callback<ApiResponse<Unit>> {
                override fun onResponse(
                    call: Call<ApiResponse<Unit>>,
                    response: Response<ApiResponse<Unit>>
                ) {
                    setLoading(false)
                    val body = response.body()

                    if (response.isSuccessful && body?.success == true) {
                        Toast.makeText(
                            this@EditarMascotaActivity,
                            body.message ?: "Mascota eliminada exitosamente.",
                            Toast.LENGTH_LONG
                        ).show()
                        startActivity(
                            Intent(this@EditarMascotaActivity, MisMascotasActivity::class.java)
                                .addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP or Intent.FLAG_ACTIVITY_SINGLE_TOP)
                        )
                        finish()
                    } else {
                        Toast.makeText(
                            this@EditarMascotaActivity,
                            body?.error ?: "Error al eliminar la mascota.",
                            Toast.LENGTH_LONG
                        ).show()
                    }
                }

                override fun onFailure(call: Call<ApiResponse<Unit>>, throwable: Throwable) {
                    setLoading(false)
                    Toast.makeText(
                        this@EditarMascotaActivity,
                        "Error al conectar con el servidor.",
                        Toast.LENGTH_LONG
                    ).show()
                }
            })
    }

    private fun validateFields(
        name: String,
        rawSpecies: String,
        species: String?,
        rawSex: String,
        sex: String?,
        rawSize: String,
        size: String?,
        rawVaccinated: String,
        vaccinated: Boolean?,
        vaccinationNotes: String?,
        rawHasMedicalConditions: String,
        hasMedicalConditions: Boolean?,
        medicalConditionsNotes: String?,
        rawAge: String
    ): Boolean {
        if (name.isBlank()) {
            binding.etNombre.error = "Ingresa el nombre."
            return false
        }

        if (rawSpecies.isBlank()) {
            binding.etTipo.error = "Ingresa el tipo de mascota."
            return false
        }

        if (species == null) {
            binding.etTipo.error = "Usa perro, gato, ave, conejo, hámster, reptil u otro."
            return false
        }

        if (rawAge.isNotBlank() && rawAge.toIntOrNull() == null) {
            binding.etEdad.error = "Ingresa una edad válida."
            return false
        }

        if (rawSex.isNotBlank() && sex == null) {
            binding.etSexo.error = "Usa macho o hembra."
            return false
        }

        if (rawSize.isNotBlank() && size == null) {
            binding.etTamano.error = "Usa pequeño, mediano o grande."
            return false
        }

        if (rawVaccinated.isNotBlank() && vaccinated == null) {
            binding.etVacunacionEstado.error = "Usa sí o no."
            return false
        }

        if (vaccinated == true && vaccinationNotes.isNullOrBlank()) {
            binding.etVacunacionDetalles.error = "Describe las vacunas."
            return false
        }

        if (rawHasMedicalConditions.isNotBlank() && hasMedicalConditions == null) {
            binding.etCondicionesMedicasEstado.error = "Usa sí o no."
            return false
        }

        if (hasMedicalConditions == true && medicalConditionsNotes.isNullOrBlank()) {
            binding.etCondicionesMedicasDetalles.error = "Describe las condiciones médicas."
            return false
        }

        return true
    }

    private fun buildCareNotes(care: String, feeding: String): String? {
        val sections = mutableListOf<String>()
        if (care.isNotBlank()) {
            sections.add("Cuidados especiales: $care")
        }
        if (feeding.isNotBlank()) {
            sections.add("Alimentación y comportamiento: $feeding")
        }
        return sections.takeIf { it.isNotEmpty() }?.joinToString("\n\n")
    }

    private fun splitCareNotes(notes: String?): Pair<String, String> {
        if (notes.isNullOrBlank()) {
            return "" to ""
        }

        var care = ""
        var feeding = ""
        notes.split("\n\n").forEach { section ->
            when {
                section.startsWith("Cuidados especiales: ") -> {
                    care = section.removePrefix("Cuidados especiales: ")
                }
                section.startsWith("Alimentación y comportamiento: ") -> {
                    feeding = section.removePrefix("Alimentación y comportamiento: ")
                }
                section.startsWith("Alimentacion y comportamiento: ") -> {
                    feeding = section.removePrefix("Alimentacion y comportamiento: ")
                }
            }
        }

        if (care.isBlank() && feeding.isBlank()) {
            care = notes
        }

        return care to feeding
    }

    private fun mapSpecies(value: String): String? = when (value.trim().lowercase()) {
        "" -> null
        "perro", "dog" -> "dog"
        "gato", "cat" -> "cat"
        "ave", "pajaro", "pájaro", "bird" -> "bird"
        "conejo", "rabbit" -> "rabbit"
        "hamster", "hámster" -> "hamster"
        "reptil", "reptile" -> "reptile"
        "otro", "other" -> "other"
        else -> null
    }

    private fun mapSex(value: String): String? = when (value.trim().lowercase()) {
        "" -> null
        "macho", "male" -> "male"
        "hembra", "female" -> "female"
        else -> null
    }

    private fun mapSize(value: String): String? = when (value.trim().lowercase()) {
        "" -> null
        "pequeno", "pequeño", "small" -> "small"
        "mediano", "medium" -> "medium"
        "grande", "large" -> "large"
        else -> null
    }

    private fun parseBooleanField(value: String): Boolean? = when (value.trim().lowercase()) {
        "" -> null
        "si", "sí", "s", "yes", "true" -> true
        "no", "n", "false" -> false
        else -> null
    }

    private fun String?.toSpanishValue(): String = when (this) {
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
        else -> this.orEmpty()
    }

    private fun Boolean?.toYesNoInput(): String = when (this) {
        true -> "Sí"
        false -> "No"
        null -> ""
    }

    private fun processImage(uri: Uri) {
        try {
            val bitmap = contentResolver.openInputStream(uri)?.use { inputStream ->
                BitmapFactory.decodeStream(inputStream)
            }

            if (bitmap == null) {
                Toast.makeText(this, "No se pudo leer la imagen.", Toast.LENGTH_SHORT).show()
                return
            }

            val maxDim = 800
            val scale = minOf(maxDim.toFloat() / bitmap.width, maxDim.toFloat() / bitmap.height)
            val scaledBitmap = if (scale < 1f) {
                val scaled = Bitmap.createScaledBitmap(bitmap, (bitmap.width * scale).toInt(), (bitmap.height * scale).toInt(), true)
                bitmap.recycle()
                scaled
            } else {
                bitmap
            }

            binding.ivPreviewImage.setImageBitmap(scaledBitmap)
            binding.ivPreviewImage.visibility = View.VISIBLE

            val outputStream = ByteArrayOutputStream()
            scaledBitmap.compress(Bitmap.CompressFormat.JPEG, 70, outputStream)
            val byteArray = outputStream.toByteArray()
            photoBase64String = Base64.encodeToString(byteArray, Base64.NO_WRAP)

        } catch (e: Exception) {
            e.printStackTrace()
            Toast.makeText(this, "Error al procesar la imagen.", Toast.LENGTH_SHORT).show()
        }
    }

    private fun setLoading(isLoading: Boolean) {
        binding.progressBar.visibility = if (isLoading) View.VISIBLE else View.GONE
        binding.btnSave.isEnabled = !isLoading
        binding.btnDelete.isEnabled = !isLoading
        binding.btnBackToDetalle.isEnabled = !isLoading
        binding.btnSeleccionarImagen.isEnabled = !isLoading
        binding.btnSave.text = if (isLoading) "Guardando..." else "Actualizar Mascota"
    }
}
