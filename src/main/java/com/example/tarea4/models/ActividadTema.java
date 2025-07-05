package com.example.tarea4.models;

import jakarta.persistence.*;

@Entity
@Table(name = "actividad_tema")
public class ActividadTema {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;


    @Enumerated(EnumType.STRING)
    private TemaEnum tema;

    @Column(name = "glosa_otro")
    private String glosaOtro;

    @ManyToOne
    @JoinColumn(name = "actividad_id")
    private Actividad actividad;


    public Integer getId()        { return id; }
    public TemaEnum getTema()     { return tema; }
    public String getGlosaOtro()  { return glosaOtro; }
    public Actividad getActividad() { return actividad; }


    public enum TemaEnum {
        música, deporte, ciencias, religión, política,
        tecnología, juegos, baile, comida, otro
    }
}
