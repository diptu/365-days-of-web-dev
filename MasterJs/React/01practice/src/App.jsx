import { useState } from "react";

function App() {
  let [count, setCount] = useState(10);
  let [msg, setMsg] = useState('');


  const add = () => {



    if (count > 19) {
      msg = "Value can't be more then 20"
      setMsg(msg);
      // setCount(20);
    }
    else {
      count = count + 1;
      setCount(count);
      console.log(count);
    }
  }

  const subtract = () => {

    if (count < 1) {
      msg = "Value can't be less then 1"
      setMsg(msg);
      // setCount(20);
    }
    else {
      count = count - 1;
      setCount(count);
      console.log(count);
    }
  }
  return (
    <div>
      <h1>Hello World</h1>
      <p>{msg}</p>
      <p>Counter : {count}</p>
      <button
        onClick={add}
      >+
      </button>

      <button
        onClick={subtract}
      >-</button>


    </div>
  )
}

export default App
