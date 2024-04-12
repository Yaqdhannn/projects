import Message from "../components/Message";
import QuizExample from "../components/QuizExample";

function Home() {
  return (
    <div>
      <h1 className="fs-1">This is the home page.</h1>
      <Message />
      <QuizExample />
    </div>
  );
}

export default Home;
