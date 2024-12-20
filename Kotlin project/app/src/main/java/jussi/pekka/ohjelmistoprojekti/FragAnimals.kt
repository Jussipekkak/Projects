package jussi.pekka.ohjelmistoprojekti

import android.os.AsyncTask
import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import androidx.navigation.fragment.navArgs
import androidx.recyclerview.widget.DividerItemDecoration
import androidx.recyclerview.widget.LinearLayoutManager
import com.google.gson.Gson
import java.io.BufferedReader
import java.io.InputStream
import java.io.InputStreamReader
import java.net.URL
import javax.net.ssl.HttpsURLConnection

//Näytetään faktoja kissoista
class FragAnimals : Fragment() {


    lateinit var recyclerView: RecyclerView
    lateinit var linearLayoutManager: LinearLayoutManager
    val argument: FragAnimalsArgs by navArgs()


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        arguments?.let {
        }
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        //Puhalletaan fragmentin layout
        val root = inflater.inflate(R.layout.fragment_frag_animals, container, false)

        //Etsitään recyclerview ja määritetään sille layout manager
        recyclerView = root.findViewById(R.id.listView)
        linearLayoutManager = LinearLayoutManager(context)
        recyclerView.layoutManager = linearLayoutManager

        //Lisätään vaakasuora erotin kunkin haetun kohteen väliin
        val divider = DividerItemDecoration(context, linearLayoutManager.orientation)
        recyclerView.addItemDecoration(divider)

        //Määritetään tietolähde ja haetaan kuinka monta faktaa halutaan.
        var url = "https://catfact.ninja/fact"
        var count = argument.howManyFacts
        //Rajoitetaan määrä 25
        if (count > 25)
        { count = 25 }
        //Suoritetaan AsyncTask haku
        HTTPAsyncTask(count).execute(url)
        return root
    }
    //Hakee datan verkosta ja palauttaa sen
    inner class HTTPAsyncTask(private val count : Int) : AsyncTask<String, Void, List<Data>>(){
        //Suorittaa haun taustalla
        override fun doInBackground(vararg p0: String?): List<Data> {
            val url = p0[0]
            val dataList = mutableListOf<Data>()
            val gson = Gson()
            //Toistaa haun käyttäjän pyytämän määrän
            repeat(count){
                val result = goOnline(url)
                val data = gson.fromJson(result, Data::class.java)//Muutetaan JSON data objektiksi
                dataList.add(data)//Lisätään haettu data listalle
            }
            return dataList
        }
        //Viedään data RecyclerView adapterille
        override fun onPostExecute(result: List<Data>) {
           super.onPostExecute(result)
            recyclerView.adapter = MyAdapter(requireContext(), result)
        }

    }
    //Tehdään GET pyyntö ja palautetaan tulos
    fun goOnline(urli: String?):String{
        val inputStream: InputStream
        val result: String
        val url: URL = URL(urli)
        val connection: HttpsURLConnection = url.openConnection() as HttpsURLConnection
        connection.connect()//Yhdistetään palvelimelle
        inputStream = connection.inputStream//Haetaan vastaus inputStreamista
        if (inputStream != null)
            result = translator(inputStream)//Muutetaan vastaus ymmärrettävään muotoon
        else
            result = "ERROR"
        connection.disconnect()
        return result
    }

    //Muuntaa Inputstream datan ymmärrettävään muotoon
    fun translator(inputStream: InputStream): String{
        val bufferedReader: BufferedReader? = BufferedReader(InputStreamReader(inputStream))
        var line: String? = bufferedReader?.readLine()
        var result: String="" //Muodostetaan tyhjä merkkijono
        //Luetaan kaikki rivit ja liitetään ne result muuttujaan
        while (line != null){
            result += line
            line = bufferedReader?.readLine()
        }
        inputStream.close()//Suljetaan inputStream
        return result.toString()//Palautetaan kokonaisuudessaan luettu merkkijono
    }
}