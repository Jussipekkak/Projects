package jussi.pekka.ohjelmistoprojekti

import android.content.Context
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import androidx.recyclerview.widget.RecyclerView.ViewHolder
import com.google.android.material.snackbar.Snackbar

// MyAdapter on RecyclerView:n adapteri, joka esittää kissoihin liittyviä faktoja.
class MyAdapter(val context: Context, val dataList: List<Data>): RecyclerView.Adapter<MyAdapter.MyHolder>() {
    // LayoutInflater, jota käytetään näkymien luomiseen.
    private val inflater: LayoutInflater = context.getSystemService(Context.LAYOUT_INFLATER_SERVICE) as LayoutInflater

    // MyHolder on ViewHolder, joka pitää sisällään yksittäisen näkymän RecyclerView:ssa.
    class MyHolder(v:View): RecyclerView.ViewHolder(v), View.OnClickListener{
        var view: View = v
        var data: Data? = null
        var content: TextView

        // Init-metodissa etsitään listan TextView ja asetetaan klikkukselle käsittelijä.
        init {
            content = view.findViewById(R.id.listcontent)// Haetaan TextView.
            view.setOnClickListener(this)// Asetetaan klikkaustapahtuman kuuntelija.
        }
        // Tämä metodi käsittelee klikkaustapahtuman ja näyttää SnackBarin, joka kertoo faktan merkkien määrän.
        override fun onClick(p0: View?) {

            Snackbar.make(content, "Length of this is ${data?.length} characters" , Snackbar.LENGTH_LONG)
                .show()

        }
        // Tämä metodi asettaa datan tähän ViewHolderiin ja asettaa factin TextViewiin.
        fun addContent(a: Data){
            this.data = a
            this.content.text = a.fact.toString() // Asetetaan tieto TextView:iin.
        }
    }
    // Tämä metodi luo uuden MyHolderin jokaiselle listan itemille.
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): MyHolder {
        val line = inflater.inflate(R.layout.list_row, parent, false) // Puhaltaa XML:n listan rivin layoutin ja luo MyHolderin.
        return MyHolder(line)
    }
    // Tämä metodi asettaa datan oikealle ViewHolderille.
    override fun onBindViewHolder(holder: MyHolder, position: Int) {
        val data = dataList[position] // Haetaan data tietystä paikasta listasta
        holder.addContent(data)  // Asetetaan data ViewHolderille.

    }
    // Tämä metodi palauttaa listan koon, eli kuinka monta itemiä RecyclerView:ssa on.
    override fun getItemCount(): Int {
        return dataList.size
    }

}