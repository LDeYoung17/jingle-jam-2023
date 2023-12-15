import "./Introduction.css";
import { Link } from "react-router-dom/cjs/react-router-dom.min";
import Typewriter from "typewriter-effect";
import elf1 from "../../Images/elf 1.png";
import lights from "../../Images/lights.png";
import bell from "../../Images/Christmas jingle bell.png";

const Introduction = () => {
  return (
    <div className="introduction">
      <h1 className="introduction__title">Welcome</h1>
      <div className="introduction__header">
        <Typewriter
          options={{
            autoStart: true,
            loop: true,
          }}
          onInit={(typewriter) => {
            typewriter
              .typeString(`Santa's optimized delivery routes`)
              .start()
              .pauseFor(3000);
          }}
        />
      </div>
      <p className="introduction__paragraph">
        I've come to talk with you again Because a vision softly creeping Left
        its seeds while I was sleeping And the vision that was planted in my
        brain Still remains Within the sound of silence In restless dreams I
        walked alone Narrow streets of cobblestone 'Neath the halo of a street
        lamp I turned my collar to the cold and damp When my eyes were stabbed
        by the flash of a neon light That split the night And touched the sound
        of silence
      </p>
      <Link to="/Main" className="introduction__button">
        Click Me For Fun
      </Link>
      <p className="introduction__copyright">
        Copyright 2023 © - All Rights Reserved by The Coding Elves
      </p>

      <img
        src={lights}
        alt="christmas lights"
        className="introduction__lights"
      />
      <img src={bell} alt="christmas bell" className="introduction__bell"></img>
      <img src={bell} alt="christmas bell" className="introduction__bell"></img>
    </div>
  );
};

export default Introduction;
