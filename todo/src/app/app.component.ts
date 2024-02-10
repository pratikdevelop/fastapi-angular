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
  });
  todo: todo[] = [];

  ngOnInit(): void {
    this.fetchData();
  }

  fetchData() {
    axios.get('http://127.0.0.1:8000').then((response) => {
      this.todo = response.data.items;
    });
  }
  addTodo(): void {
    if (!this.todoForm.value.id) {
      axios
        .post('http://127.0.0.1:8000/todo', this.todoForm.value)
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
}
