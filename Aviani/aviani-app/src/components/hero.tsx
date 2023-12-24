import videoBg from "../assets/dunes.mp4";
import "./hero.css";

function Hero() {
  return (
    <div className="hero">
      <div className="overlay"></div>
      <video src={videoBg} autoPlay loop muted />
      <div className="content">
        <h1>Aviani</h1>
        <p>visuals</p>
      </div>
    </div>
  );
}

export default Hero;
