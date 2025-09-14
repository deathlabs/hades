package main

import (
	"crypto/rand"
	"embed"
	"encoding/base64"
	"flag"
	"fmt"
	"html/template"
	"io"
	"io/fs"
	"net/http"
	"os"
	"strings"
)

//go:embed hades
var files embed.FS

type Nonce struct {
	Nonce string
}

func RandomBase64String() (string, error) {
	var (
		err         error
		randomBytes []byte = make([]byte, 16)
	)

	_, err = rand.Read(randomBytes)
	if err != nil {
		return "", err
	}

	return base64.StdEncoding.EncodeToString(randomBytes), nil
}

func middleware(nextHandler http.Handler) http.Handler {
	return http.HandlerFunc(func(writer http.ResponseWriter, request *http.Request) {
		writer.Header().Set("X-Content-Type-Options", "nosniff")
		nextHandler.ServeHTTP(writer, request)
	})
}

func main() {
	var (
		address                         string
		assets                          fs.FS
		args                            []string = os.Args[1:]
		contentSecurityPolicy           string
		contentSecurityPolicyDirectives string
		err                             error
		flagSet                         *flag.FlagSet
		indexTemplate                   *template.Template = template.Must(template.ParseFS(files, "hades/index.tmpl"))
		mux                             *http.ServeMux
		randomBase64String              string
		port                            int
		writer                          io.Writer = os.Stdout
	)

	flagSet = flag.NewFlagSet("main", flag.ContinueOnError)
	flagSet.SetOutput(writer)
	flagSet.IntVar(&port, "port", 5173, "Port to listen for requests.")

	err = flagSet.Parse(args)
	if err != nil {
		fmt.Print(err)
		os.Exit(1)
	}

	address = fmt.Sprintf(":%d", port)

	assets, err = fs.Sub(files, "hades/dist/assets")
	if err != nil {
		fmt.Print(err)
		os.Exit(1)
	}

	mux = http.NewServeMux()
	mux.HandleFunc("/", func(writer http.ResponseWriter, request *http.Request) {
		switch {
		case request.URL.Path == "/",
			request.URL.Path == "/alerts",
			request.URL.Path == "/cases",
			request.URL.Path == "/playbooks",
			strings.HasPrefix(request.URL.Path, "/alerts/"),
			strings.HasPrefix(request.URL.Path, "/cases/"),
			strings.HasPrefix(request.URL.Path, "/playbooks/"):

			// Generate a random base64 string.
			randomBase64String, err = RandomBase64String()
			if err != nil {
				fmt.Println(err)
				os.Exit(1)
			}

			// Define our Content Security Policy directives.
			contentSecurityPolicyDirectives = strings.Join([]string{
				"default-src 'self'",
				"script-src 'self' 'nonce-Nonce'",
				"style-src 'self' 'nonce-Nonce'",
				"style-src-elem	 'self' 'nonce-Nonce'",
				"frame-ancestors 'self'",
				"form-action 'self'",
				"connect-src 'self' http://localhost:8000 http://backend:8000",
			}, ";")

			// Add the random base64 string, as a nonce, to each Content Security Policy directive.
			contentSecurityPolicy = strings.ReplaceAll(contentSecurityPolicyDirectives, "Nonce", randomBase64String)

			// Set the responses HTTP headers.
			writer.Header().Set("Content-Security-Policy", contentSecurityPolicy)

			// Hydrate index.tmpl and add it to the HTTP response.
			indexTemplate.Execute(writer, Nonce{randomBase64String})
		default:
			writer.WriteHeader(http.StatusNotFound)
			writer.Write([]byte("Not Found"))
		}
	})

	mux.Handle("/assets/", http.StripPrefix("/assets/", http.FileServer(http.FS(assets))))

	err = http.ListenAndServe(address, middleware(mux))
	if err != nil {
		fmt.Print(err)
		os.Exit(1)
	}
}
