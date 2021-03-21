class Node {
    constructor(data) {
        this.data = data;
        this.next = null;
    }
}

class Queue {
    constructor() {
        this.head = null;
    }

    enqueue(data) {
        let temp = new Node(data);
        temp.next = this.head;
        this.head = temp;
    }

    dequeue() {
        let temp = this.head;
        while (temp.next.next) {
            temp = temp.next;
        }
        let element = temp.next.data;
        temp.next = null;
        return element;
    }

    printQueue() {
        let temp = this.head;
        if (temp == null) {
            console.log("Queue is empty");
        }
        while (temp) {
            console.log("Element: " + temp.data);
            temp = temp.next;
        }
        console.log("\n")
    }
}
