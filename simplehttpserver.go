package main

import (
	"fmt"
	"net/http"
	"os"
	"strconv"
)

func Log(handler http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		fmt.Printf("%s %s %s\n", r.RemoteAddr, r.Method, r.URL)
		handler.ServeHTTP(w, r)
	})
}

func main() {
	dir, _ := os.Getwd()
	h := http.FileServer(http.Dir(dir))
	port := "8000"
	if len(os.Args) >= 2 {
		port = os.Args[1]
		_, err := strconv.Atoi(port)
		if err != nil {
			fmt.Println("Error: Port must be 80-65535")
			return
		}
	}
	fmt.Printf("Serving Directory [%s] HTTP on 0.0.0.0 port %s ...\n", dir, port)
	err := http.ListenAndServe(":"+port, Log(h))
	if err != nil {
		fmt.Println("Serving error: ", err)
	}
}
