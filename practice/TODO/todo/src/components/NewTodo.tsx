import React,{useState} from 'react'

function NewTodo() {
  const [todo,setTodo] = useState({title:"", description:""});
  const {title, description }= todo;

  const handleChange = (event) => {
    const name = event.target.name;
    setTodo((oldTodo) => {
      return {...oldTodo, [name]: event.target.value}
  });
  }
  const handleSubmit = (event) =>{
    event.preventDefault();
    console.log(todo);
    setTodo({title: "", description: ""});

  }
  return (
    <div>
      <h1>NEW TODO</h1>
     
        <form method='GET' onSubmit={handleSubmit}>
            <div>
                <label htmlFor="title">Title : </label>
                <input type="text" id="fname" name="title" 
                value={title} onChange={handleChange}/>

            </div>
            <div>
                <label htmlFor="desc">Description : </label>
                <input type="text" id="desc" name="desc" 
                value={description}  onChange={handleChange}/>

            </div>
            <input type="submit" value="ADD" />
        </form>
      
    </div>
  )
}

export default NewTodo
