package com.example.stadmin.split

import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.widget.Toast
import android.graphics.Bitmap
import android.content.ContentResolver
import android.app.Activity
import android.content.Intent
import android.net.Uri
import android.os.Environment
import android.provider.MediaStore
import android.os.Environment.getExternalStorageDirectory
import android.util.Log
import android.view.View
import android.widget.ImageView
import kotlinx.android.synthetic.main.activity_main.*
import java.io.File
import android.R.attr.bitmap
import android.graphics.BitmapFactory
import android.util.Base64
import java.io.ByteArrayOutputStream
import android.os.Looper.loop
import com.airbnb.lottie.LottieAnimationView
import okhttp3.ResponseBody
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit






class MainActivity : AppCompatActivity() {

    lateinit var service: XYZService
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        floatingActionButton3.setOnClickListener { takePhoto() }

        val retrofit = Retrofit.Builder()
                .baseUrl( "https://rc0di60ov8.execute-api.us-east-1.amazonaws.com/dev/")
                .build()

        service = retrofit.create<XYZService>(XYZService::class.java)
    }


    private val TAKE_PICTURE = 1
    private var imageUri: Uri? = null



    fun takePhoto() {
        val intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
        val photo = File(Environment.getExternalStorageDirectory(), "Pic.jpg")
        intent.putExtra(MediaStore.EXTRA_OUTPUT,
                Uri.fromFile(photo))
        imageUri = Uri.fromFile(photo)
        startActivityForResult(intent, TAKE_PICTURE)

    }

    public override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        when (requestCode) {
            TAKE_PICTURE -> if (resultCode == Activity.RESULT_OK) {
                val selectedImage = imageUri
                contentResolver.notifyChange(selectedImage!!, null)
                val cr = contentResolver
                var bitmap: Bitmap
                try {
                    bitmap = android.provider.MediaStore.Images.Media
                            .getBitmap(cr, selectedImage)
                    bitmap = Bitmap.createScaledBitmap(bitmap, bitmap.width/8, bitmap.height/8, false)
                    imageView.setImageBitmap(bitmap)
                    val byteArrayOutputStream = ByteArrayOutputStream()
                    bitmap.compress(Bitmap.CompressFormat.PNG, 100, byteArrayOutputStream)
                    val byteArray = byteArrayOutputStream.toByteArray()
                    val encoded = Base64.encodeToString(byteArray, Base64.NO_WRAP)
                    Log.d("some", encoded)

                    val animationView = findViewById<View>(R.id.animation_view) as LottieAnimationView
                    Log.d("some","start")

                    //Send image
                    /*service.processImage(encoded, "hi@bye.de").enqueue(object : Callback<ResponseBody> {
                        override fun onResponse(call: Call<ResponseBody>, response: Response<ResponseBody>) {
                            animationView.cancelAnimation()
                            Log.d("some",response.body().toString())
                        }

                        override fun onFailure(call: Call<ResponseBody>, t: Throwable) {
                            Log.d("some",t.message)

                        }
                    })*/

                    animationView.setAnimation("hourglass.json")
                    animationView.loop(true)
                    animationView.playAnimation()

                } catch (e: Exception) {
                    Log.e("Camera", e.toString())
                }

            }
        }
    }




}
