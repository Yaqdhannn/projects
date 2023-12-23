import ListGroup from "./components/ListGroup";
import Button from "./components/Button";
import Alert from "./components/Alert";
import { useState } from "react";

function App() {
  let items = ["New York", "San Fran", "Tokyo", "London", "Paris"];
  let header = "Cities List";
  const handleSelectItem = (item: string) => {
    console.log(item);
  };
  
  const [AlertVisible, SetAlertVisible] = useState(false);

  return (
    <div>
      <ListGroup
        items={items}
        heading={header}
        onSelectItem={handleSelectItem}
      />
      {AlertVisible && <Alert onClose={() => SetAlertVisible(false)}>YOU PRESSED THE BUTTON NOOOO</Alert>}
      <Button onClick={() => SetAlertVisible(true)}>Click here</Button>
    </div>
  );
}

export default App;
