import sqlite3
from flask import Flask, request, jsonify
from auth import utilisateur_connecte

app = Flask(__name__)
DB = "notes.db"


@app.route("/")
def accueil():
    return jsonify({"message": "Application Notes Etudiants"})


@app.route("/health")
def health():
    return jsonify({"status": "ok", "version": "1.0"})
@app.route("/notes", methods=["GET"])
def lister_notes():

    etudiant = request.args.get("etudiant", "")
    with sqlite3.connect(DB) as con:
        rows = con.execute(
            "SELECT id, etudiant, module, note FROM notes WHERE etudiant LIKE ?",
            (f"%{etudiant}%",)
        ).fetchall()

    return jsonify([
        {"id": r[0], "etudiant": r[1], "module": r[2], "note": r[3]}
        for r in rows
    ])


@app.route("/notes/<int:note_id>", methods=["PUT"])
def modifier_note(note_id):
    utilisateur = utilisateur_connecte()
    if utilisateur is None:
        return jsonify({"error": "Authentification requise"}), 401

    if utilisateur.get("role") != "enseignant":
        return jsonify({"error": "Accès interdit"}), 403

    data = request.get_json(silent=True)

    if not data or "note" not in data:
        return jsonify({"error": "Note manquante"}), 400

    nouvelle_note = data["note"]

    if (
        isinstance(nouvelle_note, bool)
        or not isinstance(nouvelle_note, (int, float))
        or not 0 <= nouvelle_note <= 20
    ):
        return jsonify({"error": "Note invalide"}), 400

    try:
        with sqlite3.connect(DB) as con:
            resultat = con.execute(
                "SELECT module FROM notes WHERE id = ?",
                (note_id,)
            ).fetchone()
            if resultat is None:
                return jsonify({"error": "Note introuvable"}), 404

            if utilisateur.get("module") != resultat[0]:
                return jsonify({"error": "Accès interdit"}), 403

            con.execute(
                "UPDATE notes SET note = ? WHERE id = ?",
                (nouvelle_note, note_id)
            )

        return jsonify({"message": "Note modifiée avec succès"}), 200

    except sqlite3.Error:
        app.logger.exception("Erreur lors de la modification d'une note")
        return jsonify({"error": "Erreur interne"}), 500


if __name__ == "__main__":
    app.run(debug=False)
    