// this is an example from chat gpt
import React, { useState } from "react";

type Question = {
  question: string;
  answers: string[];
};

const QuizExample: React.FC = () => {
  const questions: Question[] = [
    {
      question: "What is your favorite color?",
      answers: ["Red", "Blue", "Green", "Yellow"],
    },
    {
      question: "What is your favorite food?",
      answers: ["Pizza", "Burger", "Sushi", "Pasta"],
    },
    // Add more questions here
  ];

  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);

  const handleNextQuestionClick = () => {
    setCurrentQuestionIndex(currentQuestionIndex + 1);
  };

  return (
    <div>
      <p>{questions[currentQuestionIndex].question}</p>
      {questions[currentQuestionIndex].answers.map((answer, index) => (
        <button key={index} onClick={handleNextQuestionClick}>
          {answer}
        </button>
      ))}
    </div>
  );
};

export default QuizExample;
