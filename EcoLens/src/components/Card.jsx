
function Card(props) { 

// eslint-disable-next-line react/prop-types
const {title, description} = props; 
  return (
    
    <article className="card">
        <header>
          <h2 className="heading">{title}</h2>
        </header>
        <img src="todo.png" alt="To DO List" className="thumbnail" />
        <div className="content">
          <p> {description} </p>
        </div>
    </article>

  )
 }
 export default Card