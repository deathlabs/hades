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
		assets                          fs.FS
		args                            []string = os.Args[1:]
		backend                         string
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
	flagSet.StringVar(&backend, "b", "", "The backend's IP address or domain name (e.g., backend).")
	flagSet.IntVar(&port, "p", 0, "The port to listen to for requests.")

	err = flagSet.Parse(args)
	if err != nil {
		fmt.Print(err)
		os.Exit(1)
	}

	if backend == "" {
		fmt.Print("[x] An argument for the 'b' parameter is required")
		os.Exit(1)
	}

	if port == 0 {
		fmt.Print("[x] An argument for the 'p' parameter is required")
		os.Exit(1)
	}

	assets, err = fs.Sub(files, "hades/dist/assets")
	if err != nil {
		fmt.Print(err)
		os.Exit(1)
	}

	mux = http.NewServeMux()
	mux.HandleFunc("/", func(writer http.ResponseWriter, request *http.Request) {
		switch {
		case request.URL.Path == "/",
			strings.HasPrefix(request.URL.Path, "/injects/"):

			// Generate a random base64 string.
			randomBase64String, err = RandomBase64String()
			if err != nil {
				fmt.Println(err)
				os.Exit(1)
			}

			// Define our Content Security Policy directives.
			contentSecurityPolicyDirectives = fmt.Sprintf(
				strings.Join([]string{
					"default-src 'self'",
					"script-src 'self' 'nonce-Nonce'",
					"style-src 'self' 'nonce-Nonce'",
					"style-src-elem	 'self' 'nonce-Nonce'",
					"frame-ancestors 'self'",
					"form-action 'self'",
					"connect-src 'self' %s ws://%s",
				}, ";"),
				backend, backend)

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

	err = http.ListenAndServe(fmt.Sprintf(":%d", port), middleware(mux))
	if err != nil {
		fmt.Print(err)
		os.Exit(1)
	}
}
