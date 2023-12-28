import videoBg from "../assets/dunes.mp4";
import "../index.css";

function Hero() {
  return (
    <div className="relative w-screen h-screen">
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
          <h1 className="text-one text-6xl">Aviani visuals</h1>
          <p className="text-three mx-40 text-lg">
            Lorem ipsum dolor sit amet, consectetur adipisicing elit.
            Dignissimos consequuntur labore aperiam magnam, dolor ad numquam,
            exercitationem ratione excepturi qui iure quasi praesentium et
            dolores reprehenderit nostrum atque eos officia?
          </p>
        </div>
      </div>
    </div>
  );
}

export default Hero;
