<?php

namespace App\Http\Controllers;

use App\UseCases\LivroUseCase;
use App\Http\Requests\StoreLivroRequest;
use App\Http\Requests\UpdateLivroRequest;
use App\Http\Resources\LivroResource;

/**
 * @OA\Tag(
 *     name="Livros",
 *     description="Endpoints para gerenciar livros"
 * )
 */
class LivroController extends Controller
{
    protected $service;

    public function __construct(LivroUseCase $service)
    {
        $this->service = $service;
    }

    /**
     * @OA\Get(
     *      path="/api/livros",
     *      operationId="getLivrosList",
     *      tags={"Livros"},
     *      summary="Lista todos os livros",
     *      description="Retorna uma lista de livros",
     *      security={{"apiAuth":{}}},
     *      @OA\Response(
     *          response=200,
     *          description="Operação bem-sucedida",
     *          @OA\JsonContent(
     *              type="array",
     *              @OA\Items(ref="#/components/schemas/Livro")
     *          )
     *       )
     *     )
     */
    public function index()
    {
        $livros = $this->service->getAll();
        return LivroResource::collection($livros);
    }

    /**
     * @OA\Post(
     *      path="/api/livros",
     *      operationId="storeLivro",
     *      tags={"Livros"},
     *      summary="Cria um novo livro",
     *      description="Cria um novo livro e o retorna",
     *      security={{"apiAuth":{}}},
     *      @OA\RequestBody(
     *          required=true,
     *          @OA\JsonContent(
     *              required={"titulo", "autor_id", "categoria_id"},
     *              @OA\Property(property="titulo", type="string", example="Dom Casmurro"),
     *              @OA\Property(property="autor_id", type="integer", example=1),
     *              @OA\Property(property="categoria_id", type="integer", example=1)
     *          )
     *      ),
     *      @OA\Response(
     *          response=201,
     *          description="Livro criado com sucesso",
     *          @OA\JsonContent(ref="#/components/schemas/Livro")
     *      ),
     *      @OA\Response(
     *          response=422,
     *          description="Erro de validação"
     *      )
     * )
     */
    public function store(StoreLivroRequest $request)
    {
        $livro = $this->service->create($request->validated());
        return new LivroResource($livro);
    }

    /**
     * @OA\Get(
     *      path="/api/livros/{id}",
     *      operationId="getLivroById",
     *      tags={"Livros"},
     *      summary="Obtém um livro específico",
     *      description="Retorna os dados de um livro",
     *      security={{"apiAuth":{}}},
     *      @OA\Parameter(
     *          name="id",
     *          description="ID do Livro",
     *          required=true,
     *          in="path",
     *          @OA\Schema(
     *              type="integer"
     *          )
     *      ),
     *      @OA\Response(
     *          response=200,
     *          description="Operação bem-sucedida",
     *          @OA\JsonContent(ref="#/components/schemas/Livro")
     *      ),
     *      @OA\Response(
     *          response=404,
     *          description="Livro não encontrado"
     *      )
     * )
     */
    public function show($id)
    {
        $livro = $this->service->find($id);
        if ($livro) {
            return new LivroResource($livro);
        }
        return response()->json(['message' => 'Livro não encontrado'], 404);
    }

    /**
     * @OA\Put(
     *      path="/api/livros/{id}",
     *      operationId="updateLivro",
     *      tags={"Livros"},
     *      summary="Atualiza um livro existente",
     *      description="Atualiza os dados de um livro e o retorna",
     *      security={{"apiAuth":{}}},
     *      @OA\Parameter(
     *          name="id",
     *          description="ID do Livro",
     *          required=true,
     *          in="path",
     *          @OA\Schema(
     *              type="integer"
     *          )
     *      ),
     *      @OA\RequestBody(
     *          required=true,
     *          @OA\JsonContent(
     *              @OA\Property(property="titulo", type="string", example="Memórias Póstumas de Brás Cubas"),
     *              @OA\Property(property="autor_id", type="integer", example=1),
     *              @OA\Property(property="categoria_id", type="integer", example=1)
     *          )
     *      ),
     *      @OA\Response(
     *          response=200,
     *          description="Livro atualizado com sucesso",
     *          @OA\JsonContent(ref="#/components/schemas/Livro")
     *      ),
     *      @OA\Response(
     *          response=404,
     *          description="Livro não encontrado"
     *      )
     * )
     */
    public function update(UpdateLivroRequest $request, $id)
    {
        $livro = $this->service->update($id, $request->validated());
        if ($livro) {
            return new LivroResource($livro);
        }
        return response()->json(['message' => 'Livro não encontrado'], 404);
    }

    /**
     * @OA\Delete(
     *      path="/api/livros/{id}",
     *      operationId="deleteLivro",
     *      tags={"Livros"},
     *      summary="Deleta um livro",
     *      description="Deleta um livro existente",
     *      security={{"apiAuth":{}}},
     *      @OA\Parameter(
     *          name="id",
     *          description="ID do Livro",
     *          required=true,
     *          in="path",
     *          @OA\Schema(
     *              type="integer"
     *          )
     *      ),
     *      @OA\Response(
     *          response=200,
     *          description="Livro deletado com sucesso"
     *      ),
     *      @OA\Response(
     *          response=404,
     *          description="Livro não encontrado"
     *      )
     * )
     */
    public function destroy($id)
    {
        if ($this->service->delete($id)) {
            return response()->json(null, 204);
        }
        return response()->json(['message' => 'Livro não encontrado'], 404);
    }
}
