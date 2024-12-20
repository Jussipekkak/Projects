package jussi.pekka.ohjelmistoprojekti

import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import androidx.navigation.fragment.findNavController
import androidx.navigation.fragment.navArgs

//Fragmentti kysyy käyttäjältä montako faktaa haetaan
class FragSecond : Fragment() {

    //haetaan ensimmäisen fragmentin hakema tieto
    val argument: FragSecondArgs by navArgs()

    //Alustetaan tarvittavat elementit
    lateinit var textView: TextView
    lateinit var editText: EditText
    lateinit var button: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        arguments?.let {
        }
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        //Puhalletaan layout esille
        val root = inflater.inflate(R.layout.fragment_frag_second, container, false)

        //Initialisoidaan elementeille oikeat lähteet
        textView = root.findViewById(R.id.hellotext)
        editText = root.findViewById(R.id.numberinput)
        button = root.findViewById(R.id.button1FragSecond)

        //Käytetään käyttäjän edellisessä fragmentissa antamaa syötettä ja näytetään se
        val name = argument.username
        textView.text = "Hello $name"


        //Luodaan napille kuuntelija, ja tallennetaan käyttäjän antama luku halutulle faktamäärälle.
        //Mikäli käyttäjä ei anna lukua, ohjelma palauttaa yhden faktan
        button.setOnClickListener{
            val howManyFacts = editText.text.toString().toIntOrNull() ?:1
            val action = FragSecondDirections.actionFragSecondToFragAnimals(howManyFacts = howManyFacts)//Käyttäjä ohjataan seuraavaan fragmenttiin
            findNavController().navigate(action)
        }
        return root
    }
}