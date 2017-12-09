package com.example.stadmin.split;

import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.http.Field;
import retrofit2.http.Headers;
import retrofit2.http.POST;

/**
 * Created by STAdmin on 09.12.2017.
 */

public interface XYZService {

    @Headers("content-type : application/json")
    @POST("parseImage")
    Call<ResponseBody> processImage(@Field("data") String base64Image, @Field("email") String mail);
}
