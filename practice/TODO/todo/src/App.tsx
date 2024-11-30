import TodoList from "./components/TodoList"
import "bootstrap/dist/css/bootstrap.min.css";
import "font-awesome/css/font-awesome.min.css";
import style from "./style.css";
import NewTodo from "./components/NewTodo";
const sample = [
  {
  id: 1,
  title: "Sand Analytics Research",
  description: "Work on sand analytics Project",
},
{
  id: 2,
  title: "DL",
  description: "Daily DL Practice",
},
{
  id: 3,
  title: "web-dev",
  description: "365 days of web development",
}

]
function App() {
 

  return (
    <div className="container">
      <h1>TODO APP</h1>
      <NewTodo />
      <TodoList todos={sample} />
     
    </div>
  )
}

export default App
