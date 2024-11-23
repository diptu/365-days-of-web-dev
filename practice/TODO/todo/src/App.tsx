import TodoList from "./components/TodoList"

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
    <div>
      <TodoList todos={sample} />
     
    </div>
  )
}

export default App
