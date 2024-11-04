/* eslint-disable react/jsx-key */
import Card from './components/Card'
import Data from './data.json'
import { v4 as uuidv4 } from 'uuid';

function App() {
 

  return (
    <>
    <div className="cards">
      { Data.map((todo) => (
        <Card key={uuidv4()} title={todo.DAY} description = {
          todo.tasks.map((task) => 
            <div>
            <h3>{task.practice}- {task.category}</h3>
            <p>{task.description}</p>
            </div>
          )}
        
        />))}
   
 
    </div>
   
    </>
  )
}

export default App
