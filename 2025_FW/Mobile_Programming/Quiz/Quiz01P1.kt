package com.example.hw01

import android.util.Log;

import android.os.Bundle
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.util.LogWriter
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import java.util.Arrays

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        fun isPrime(x: Int): Boolean { // Define “isPrime” function
            if (x % 2 == 0){
                return false
            }else if (x % 3 == 0)
        }

        val numbers = IntArray(10) // Generate a list
        for (i in 1.. 10){
            numbers[i] = (1..100).random()
        }
        println("Original List: $numbers") // Print the original list

        val primeNumbers = numbers.filter… // Filter the list

        println("Prime Numbers: $primeNumbers") // Print the prime number list


    }
}