import videoBg from "../assets/dunes.mp4";
import "../index.css";

function Hero() {
  return (
    <div className="relative w-screen h-96">
      {/* Video */}
      <video
        className="w-full h-full object-cover"
        src={videoBg}
        autoPlay
        loop
        muted
      />

      {/* Overlay */}
      <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50">
        {/* Text */}
        <div className="text-center text-white">
          <h1 className="text-one">Aviani visuals</h1>
          <p className="text-three">
            Lorem ipsum, dolor sit amet consectetur adipisicing elit. Corrupti
            sunt porro quo ut qui repellendus, voluptatum soluta consequuntur
            asperiores omnis? Nostrum nihil ipsa sunt, cum dolor sapiente id
            distinctio accusantium?
          </p>
        </div>
      </div>
    </div>
  );
}

export default Hero;
