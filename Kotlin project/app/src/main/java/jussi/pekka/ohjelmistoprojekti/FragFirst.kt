package jussi.pekka.ohjelmistoprojekti

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import androidx.navigation.fragment.findNavController

//Luodaan ensimmäinen fragmentti, joka pyytää käyttäjän nimeä, ja siirtää sen seuraavaan fragmenttiin
class FragFirst : Fragment() {

    //Luodaan tarvittavat elementit
    lateinit var button: Button
    lateinit var nameinput: EditText

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
        val root = inflater.inflate(R.layout.fragment_frag_first, container, false)

        //Haetaan elementeille oikeat viittaukset
        button = root.findViewById(R.id.buttonFragFirst)
        nameinput = root.findViewById(R.id.inputFragment1)

            //Luodaan kuuntelija napille, joka avaa seuraavan fragmentin
        button.setOnClickListener{
            val action = FragFirstDirections.actionFragFirstToFragSecond(nameinput.text.toString())
            findNavController().navigate(action)
        }
        return root
    }
}