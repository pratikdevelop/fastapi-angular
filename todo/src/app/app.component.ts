import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import axios from 'axios';
import {
  FormControl,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
} from '@angular/forms';

interface todo {
  id: number;
  todo_description: string;
  todo_name: string;
  todo_image: string;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, ReactiveFormsModule, FormsModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class AppComponent {
  todoForm: FormGroup = new FormGroup({
    id: new FormControl(),
    todo_name: new FormControl(''),
    todo_description: new FormControl(''),
    todo_image: new FormControl(''),
    file: new FormControl(File),
  });
  todoImage!: File;
  todo: todo[] = [];

  ngOnInit(): void {
    this.fetchData();
  }

  fetchData() {
    axios.get('http://127.0.0.1:8000').then((response) => {
      this.todo = response.data.items;
    });
  }

  onFileChange(event: any) {
    console.log(event.target.files);
    if (event.target.files.length > 0) {
      const file = event.target.files[0];
      this.todoImage = file;
    }
    console.log(this.todoImage);
    
  }
  addTodo(): void {
    console.log('todo',  );
    const formData = new FormData();
    formData.append('todo_name', this.todoForm.value.todo_name);
    formData.append('todo_description', this.todoForm.value.todo_description);
    // formData.append('file_name', this.todoForm.value.todo_image);
    formData.append('todo_image', this.todoImage);
    // this.todoForm.get("file")?.setValue(this.todoImage);
    
    
    if (!this.todoForm.value.id) {
      axios
        .post('http://127.0.0.1:8000/todo',formData)
        .then((response) => {
          this.todo.push(response.data);
        });
    } else {
      axios
        .put(
          'http://127.0.0.1:8000/todo/' + this.todoForm.value.id,
          this.todoForm.value
        )
        .then((response) => {
          console.log(response.data);
          
          let index = this.todo.findIndex((td) => {
            return td.id === response.data.id;
          });
          console.log(index)
          this.todo[index] = response.data;
        });

    }
    this.todoForm.reset();
  }

  editTodo(todo: todo): void {
    this.todoForm.patchValue(todo);
  }

  deleteTodo(todo:todo): void {
    axios.delete('http://127.0.0.1:8000/todo/' + todo.id).then((response)=>{
       let index = this.todo.findIndex(to => {return to.id = todo.id})
       this.todo.splice(index, 1)
    })
  }

  getFile(image_name: string): string {
    return 'http://127.0.0.1:8000/files/'+ image_name
  }
}
