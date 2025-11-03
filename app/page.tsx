"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

export default function Home() {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  const [nomeDoenca, setNomeDoenca] = useState<string | null>(null);
  const [tratamento, setTratamento] = useState<string | null>(null);

  // Função para carregar imagem
  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type === "image/jpeg") {
      setSelectedImage(file);
      setPreview(URL.createObjectURL(file));
      setResult(null);
      setNomeDoenca(null);
      setTratamento(null);
    } else {
      alert("Por favor, selecione uma imagem JPG.");
    }
  };

  // Função para enviar imagem para a API
  const handleSearchDisease = async () => {
    if (!selectedImage) {
      alert("Carregue uma imagem primeiro!");
      return;
    }

    setLoading(true);
    setResult(null);
    setNomeDoenca(null);
    setTratamento(null);

    try {
      const formData = new FormData();
      formData.append("file", selectedImage);

      // 🔗 Chamada à API (substituir pela URL real)
      /* const response = await fetch("/api/detectar-doenca", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Erro ao processar a imagem");

      const data = await response.json(); */

      // 🔍 Exemplo de resposta esperada da API:
      const data = {
        nome: "Mancha foliar",
        tratamento: "Aplicar fungicida",
        resultado: "Doença detectada",
      };

      setResult(data.resultado || "Análise concluída.");
      setNomeDoenca(data.nome || "—");
      setTratamento(data.tratamento || "—");
    } catch (error) {
      console.error(error);
      setResult("Erro ao analisar a imagem.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4 bg-gradient-to-b from-blue-50 to-blue-100">
      <motion.div
        className="bg-white shadow-xl rounded-2xl p-6 w-full max-w-md text-center"
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <img
          src="logo-Agrolens2.jpg"
          alt="Your Image"
          className="mx-auto mb-4"
        />
        <h1 className="text-2xl font-bold mb-6 text-gray-700">
          🌿 Reconhecimento de Doenças de Plantas por Imagem
        </h1>

        {/* Upload de imagem */}
        <input
          type="file"
          accept="image/jpeg"
          onChange={handleImageUpload}
          className="hidden"
          id="upload"
        />
        <label
          htmlFor="upload"
          className="cursor-pointer bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-xl shadow-md transition duration-300 inline-block"
        >
          Carregar Imagem JPG
        </label>

        {/* Pré-visualização */}
        <AnimatePresence>
          {preview && (
            <motion.div
              key="preview"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="mt-4"
            >
              <img
                src={preview}
                alt="Pré-visualização"
                className="w-full rounded-xl border mt-2 shadow-sm"
              />
            </motion.div>
          )}
        </AnimatePresence>

        {/* Botão de pesquisa */}
        <button
          onClick={handleSearchDisease}
          disabled={!selectedImage || loading} // ← agora só habilita após carregar imagem
          className={`mt-6 px-4 py-2 rounded-xl shadow-md w-full transition duration-300 flex items-center justify-center gap-2
            ${
              !selectedImage || loading
              ? "bg-gray-300 cursor-not-allowed"
              : "bg-green-500 hover:bg-green-600 text-white"
            }`}
        >
          {loading ? (
            <>
              <span className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full"></span>
              <span>Analisando imagem...</span>
            </>
          ) : (
            "Pesquisar Doença"
          )}
        </button>

        {/* Resultado principal */}
        <AnimatePresence>
          {result && (
            <motion.div
              key="resultado"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.5 }}
              className="text-2xl font-bold py-6 text-gray-700"
            >
              {result}
            </motion.div>
          )}
        </AnimatePresence>

        {/* 🧠 Nome da doença */}
        {nomeDoenca && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="bg-blue-50 border border-blue-200 rounded-xl p-3 text-left"
          >
            <h2 className="text-sm text-gray-500">Nome da Doença:</h2>
            <p className="text-base font-semibold text-blue-700">
              {nomeDoenca}
            </p>
          </motion.div>
        )}

        {/* 💊 Tratamento sugerido */}
        {tratamento && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="mt-3 bg-green-50 border border-green-200 rounded-xl p-3 text-left"
          >
            <h2 className="text-sm text-gray-500">Tratamento Recomendado:</h2>
            <p className="text-base font-medium text-green-700">{tratamento}</p>
          </motion.div>
        )}
      </motion.div>

      <footer className="mt-6 text-sm text-gray-500">
        © 2025 AgroLensLabs – Todos os direitos reservados.
      </footer>
    </div>
  );
}
