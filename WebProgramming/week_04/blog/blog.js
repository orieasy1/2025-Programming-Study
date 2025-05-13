
document.addEventListener("DOMContentLoaded",()=>{

    const btnAddEntry = qs("button");
    btnAddEntry.onclick = addEntry;
});

/**
 * Returns a new <article> html element containing the date and thoughts in the
 * parameters
 * 
 */
function addEntry(){

    let date = id("date").value;
    let thoughts = id("entry").value;
    if (date=="" || thoughts==""){
        alert("Enter some content to post.");
        return;
    }
    //create elements I will use
    let post = document.createElement("article");
    let title = document.createElement("h1");
    let content = document.createElement("p");

    //set properties for each element
    title.textContent = "Date: " + date;
    content.textContent = "Entry: " + thoughts;

    //append to the article element I will return
    post.appendChild(title);
    post.appendChild(content);

    //set elemetn style
    post.classList.add("post") // check css file for this

    //attach behavior for double click
    post.addEventListener("dblclick", removePost);

    // add post to #posts container
    id("posts").appendChild(post);

    //clear up Date and Thoughts textboxes
    id("date").value = "";
    id("entry").value = "";

    // check if maximum posts are reached    
    checkNumPosts();    
}

/**
 * removes the selected blog post
 */
function removePost() {
this.remove(); // this refers to the object to which this function is attached to
checkNumPosts();
}

/**
 * check if there are at most 3 posts and enable or disable
 * the add entry button 
 */
function checkNumPosts() {
    let posts = qsa(".post");
    let numPosts = posts.length;
    console.log(numPosts);
    let addEntryBtn = qs("button");
    if (numPosts>=3) {
      addEntryBtn.disabled = true;
    } else {
      addEntryBtn.disabled = false;
    }
  }


  /**
   * Returns the element that has the ID attribute with the specified value.
   * @param {string} name - element ID.
   * @returns {object} - DOM object associated with id.
   */
  function id(id) {
    return document.getElementById(id);
  }

  /**
   * Returns first element matching selector.
   * @param {string} selector - CSS query selector.
   * @returns {object} - DOM object associated selector.
   */
  function qs(selector) {
    return document.querySelector(selector);
  }

  /**
   * Returns the array of elements that match the given CSS selector.
   * @param {string} query - CSS query selector
   * @returns {object[]} array of DOM objects matching the query.
   */
   function qsa(query) {
    return document.querySelectorAll(query);
  }