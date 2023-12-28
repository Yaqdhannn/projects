import brand from "../assets/talib-head.png";

function Navbar() {
  return (
    <nav className="inset-y-3 inset-x-1/2 transform -translate-x-1/2 z-10 fixed w-screen max-w-screen-lg h-12 items-center flex border-2 rounded-2xl bg-black bg-opacity-20 border-one">
      <div className="w-12 mx-2">
        <img src={brand} alt="Aviani Brand"/>
      </div>
      <ul className="flex justify-center flex-1 space-x-8 text-lg">
        <li className="text-three flex-none">Home</li>
        <li className="text-three flex-none">Projects</li>
        <li className="text-three flex-none">About us</li>
        <li className="text-three flex-none">Contact us</li>
      </ul>
    </nav>
  );
}

export default Navbar;
